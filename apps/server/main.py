import os
import sys
import json
import traceback
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
from twilio.rest import Client
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ConversationInitiationData
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from twilio_audio import TwilioAudioInterface
from starlette.websockets import WebSocketDisconnect, WebSocketState
from urllib.parse import quote
from pydantic import BaseModel
from era_config import get_era_session_variables

# Add packages directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "packages", "shared-py"))

# Import voice and agent managers
from voice_manager import VoiceManager
from agent_manager import AgentManager
from first_message_manager import FirstMessageManager

load_dotenv()

DEBUG_LOGS = os.getenv("DEBUG_LOGS", "false").lower() == "true"

# Load environment variables
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Check for required environment variables
if not ELEVENLABS_API_KEY:
    raise ValueError("Missing required ElevenLabs environment variables")

app = FastAPI(title="Twilio-ElevenLabs Integration Server")

# Initialize voice and agent managers globally
voice_manager = VoiceManager()
agent_manager = AgentManager()
first_message_manager = FirstMessageManager()

print(f"🎤 Voice Manager initialized with {voice_manager.get_voice_statistics()}")
print(f"🤖 Agent Manager initialized with {agent_manager.get_agent_statistics()}")
print(f"💬 First Message Manager initialized with {first_message_manager.get_statistics()['total_eras']} eras")

# Pydantic models for request bodies
class OutboundCallRequest(BaseModel):
    to: str
    lang: str = "en"  # Default to English
    year: int = 2024  # Default to current year

# Helper func to get Twilio client
def get_twilio_client():
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        raise HTTPException(status_code=500, detail="Twilio credentials not configured")
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.get("/")
async def root():
    return {"message": "Twilio-ElevenLabs Integration Server"}

@app.post("/outbound-call")
async def outbound_call(
    call_request: OutboundCallRequest,
    request: Request = None,
    twilio_client: Client = Depends(get_twilio_client)
):
    if not TWILIO_PHONE_NUMBER:
        raise HTTPException(status_code=500, detail="Twilio phone number not configured")

    try:
        # Create URL for TwiML with URL-encoded parameters for language and year
        twiml_url = f"https://{request.headers.get('host')}/outbound-call-twiml?lang={quote(call_request.lang)}&year={call_request.year}"

        # Initiate the call via Twilio
        call = twilio_client.calls.create(
            from_=TWILIO_PHONE_NUMBER,
            to=call_request.to,
            url=twiml_url
        )

        return JSONResponse({
            "success": True,
            "message": "Call initiated",
            "callSid": call.sid,
            "parameters": {
                "to": call_request.to,
                "lang": call_request.lang,
                "year": call_request.year
            }
        })
    except Exception as e:
        print(f"Error initiating outbound call: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Failed to initiate call",
                "details": str(e)
            }
        )

@app.get("/outbound-call-twiml")
@app.post("/outbound-call-twiml")
async def outbound_call_twiml(
    request: Request,
    lang: str = "en",
    year: int = 2024
):
    response = VoiceResponse()
    connect = Connect()

    # Create a Stream with custom parameters for language and year
    # Note: Twilio doesn't pass query parameters to WebSocket, so we use custom parameters instead
    websocket_url = f"wss://{request.headers.get('host')}/outbound-media-stream"
    stream = Stream(url=websocket_url)
    
    # Add custom parameters that Twilio will pass in the 'start' event
    stream.parameter(name="lang", value=lang)
    stream.parameter(name="year", value=str(year))
    
    print(f"🔗 TwiML WebSocket URL: {websocket_url}")
    print(f"📋 Custom parameters: lang={lang}, year={year}")

    connect.append(stream)
    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml")

@app.websocket("/outbound-media-stream")
async def handle_outbound_media_stream(websocket: WebSocket):
    await websocket.accept()
    
    print(f"Outbound WebSocket connection opened - waiting for Twilio start event with custom parameters...")

    # Variables to track the call
    stream_sid = None
    call_sid = None
    audio_interface = TwilioAudioInterface(websocket)
    eleven_labs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    conversation = None

    try:
        async for message in websocket.iter_text():
            if not message:
                print("Empty message received")
                continue

            if DEBUG_LOGS:
                print(f"Raw WebSocket message: {message[:200]}...") 

            data = json.loads(message)
            event_type = data.get("event")

            # Handle the start event
            if event_type == "start":
                stream_sid = data["start"]["streamSid"]
                call_sid = data["start"]["callSid"]
                custom_parameters = data["start"].get("customParameters", {})

                # Extract language and year from Twilio custom parameters
                lang = custom_parameters.get("lang", "en")
                year = int(custom_parameters.get("year", 2024))

                # Set stream_id (used by TwilioAudioInterface for outbound audio)
                audio_interface.stream_id = stream_sid

                print(f"Outbound call started - StreamSid: {stream_sid}, CallSid: {call_sid}")
                print(f"Call parameters - Language: {lang}, Year: {year}")

                # Get era-specific configuration
                session_vars = get_era_session_variables(year, lang)
                
                print(f"Era configuration: {session_vars['era_name']} ({session_vars['time_period']})")

                # Initialize the conversation
                try:
                    # Get randomized voice for the language (era-agnostic randomization)
                    # Voice characteristics (speed, stability, style) come from era_config.py
                    selected_voice = voice_manager.get_random_voice_for_language(lang)
                    voice_id = selected_voice['id'] if selected_voice else None
                    
                    # Fallback to environment variable voice pools if JSON selection fails
                    if not voice_id:
                        voice_id = voice_manager.get_voice_id_from_env(lang)
                        if voice_id:
                            print(f"🔄 Using fallback voice from env: {voice_id[:8]}...")
                    
                    # Get randomized agent (era-agnostic)
                    selected_agent = agent_manager.get_random_agent()
                    agent_id_to_use = agent_manager.get_agent_id(selected_agent) if selected_agent else ELEVENLABS_AGENT_ID_1
                    
                    # Fallback to base agent if random selection fails
                    if not agent_id_to_use:
                        agent_id_to_use = ELEVENLABS_AGENT_ID
                        print(f"🔄 Using fallback base agent: {agent_id_to_use[:8]}...")
                    
                    print(f"🎯 Using agent ID: {agent_id_to_use[:8]}... ({selected_agent['name'] if selected_agent else 'fallback'})")
                    print(f"🎤 Using voice ID: {voice_id[:8] if voice_id else 'default'}... ({selected_voice['name'] if selected_voice else 'agent default'})")
                    
                    # Create dynamic variables for the agent's system prompt (exclude voice_settings)
                    dynamic_vars = {k: v for k, v in session_vars.items() if k != 'voice_settings'}
                    
                    # Add voice metadata for character consistency
                    if selected_voice:
                        dynamic_vars["voice_gender"] = selected_voice.get('gender', 'unknown')
                        dynamic_vars["voice_age_range"] = selected_voice.get('age_range', 'unknown')
                    
                    # Create conversation config override combining:
                    # 1. Era-specific voice settings (from era_config.py)
                    # 2. Randomized voice_id (from voice_manager)
                    voice_settings = session_vars['voice_settings'].copy()
                    
                    # Get random first message for this era and language
                    first_message = first_message_manager.get_random_first_message(
                        era_name=session_vars['era_name'], 
                        language=lang
                    )
                    
                    # Use the official ElevenLabs documentation structure exactly
                    conversation_override = {
                        "agent": {},
                        "tts": {}
                    }
                    
                    # Add first message override if available
                    if first_message:
                        conversation_override["agent"]["first_message"] = first_message
                        #print(f"💬 First message override set: {first_message[:50]}...")
                    
                    # Add voice_id if available (official docs show this is supported)
                    if voice_id:
                        conversation_override["tts"]["voice_id"] = voice_id
                        print(f"🎤 Voice ID override set: {voice_id}")
                    
                    # Add other voice settings - testing which ones cause issues
                    # Note: These might need to be enabled in agent security settings
                    voice_settings_to_test = {
                        "stability": voice_settings.get("stability"),
                        "similarity_boost": voice_settings.get("similarity_boost"), 
                        "speed": voice_settings.get("speed")
                        # Excluding 'style' as it wasn't in the screenshot
                    }
                    
                    # Add voice settings to override
                    conversation_override["tts"].update(voice_settings_to_test)
                    
                    print(f"🔍 Dynamic variables: {dynamic_vars}")
                    print(f"🔧 Voice settings from era config: {voice_settings}")
                    print(f"📡 Conversation override structure: {json.dumps(conversation_override, indent=2)}")
                    #print(f"⚠️  Important: Voice overrides must be enabled in ElevenLabs agent security settings")
                    
                    # Try with both dynamic variables and conversation overrides
                    try:
                        config = ConversationInitiationData(
                            dynamic_variables=dynamic_vars,
                            conversation_config_override=conversation_override
                        )
                        
                        conversation = Conversation(
                            client=eleven_labs_client,
                            agent_id=agent_id_to_use,
                            config=config,
                            requires_auth=True,
                            audio_interface=audio_interface,
                            callback_agent_response=lambda text: print(f"Agent ({session_vars['era_name']}/{selected_agent['name'] if selected_agent else 'default'}): {text}"),
                            callback_user_transcript=lambda text: print(f"User: {text}"),
                        )
                        print("✅ Created conversation with dynamic variables and voice overrides")
                    except Exception as config_error:
                        print(f"❌ Error with voice override config: {config_error}")
                        print(f"📋 Error details: {str(config_error)}")
                        print("🔄 Trying without voice overrides...")
                        
                        try:
                            # Fallback: Try with just dynamic variables, no voice overrides
                            config_fallback = ConversationInitiationData(
                                dynamic_variables=dynamic_vars
                            )
                            
                            conversation = Conversation(
                                client=eleven_labs_client,
                                agent_id=agent_id_to_use,
                                config=config_fallback,
                                requires_auth=True,
                                audio_interface=audio_interface,
                                callback_agent_response=lambda text: print(f"Agent (no voice override/{selected_agent['name'] if selected_agent else 'default'}): {text}"),
                                callback_user_transcript=lambda text: print(f"User: {text}"),
                            )
                            print("✅ Created conversation with dynamic variables only (no voice overrides)")
                        except Exception as fallback_error:
                            print(f"❌ Error even without voice overrides: {fallback_error}")
                            print("🔄 Falling back to basic conversation...")
                            
                            # Final fallback: Basic conversation
                            conversation = Conversation(
                                client=eleven_labs_client,
                                agent_id=agent_id_to_use,
                                requires_auth=True,
                                audio_interface=audio_interface,
                                callback_agent_response=lambda text: print(f"Agent (basic/{selected_agent['name'] if selected_agent else 'default'}): {text}"),
                                callback_user_transcript=lambda text: print(f"User: {text}"),
                            )

                    # Start the conversation session
                    conversation.start_session()
                    
                    print(f"ElevenLabs conversation started successfully\n")
                    #print(f"Era: {session_vars['era_name']} | Language: {lang} | Year: {year}")
                except Exception as e:
                    print(f"Error starting ElevenLabs conversation: {str(e)}")
                    traceback.print_exc()

            # Handle incoming media
            elif event_type == "media" and conversation:
                try:
                    await audio_interface.handle_twilio_message(data)
                except Exception as e:
                    print(f"Error handling audio: {str(e)}")
                    traceback.print_exc()

            # Handle stop event
            elif event_type == "stop":
                print(f"Call ended - StreamSid: {stream_sid}")
                if conversation:
                    try:
                        conversation.end_session()
                        print("ElevenLabs conversation ended")
                    except Exception as e:
                        print(f"Error ending conversation: {str(e)}")

    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        traceback.print_exc()

    finally:
        if conversation:
            try:
                conversation.end_session()
                conversation.wait_for_session_end()
                print("Conversation cleanup completed")
            except Exception as e:
                print(f"Error in conversation cleanup: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)