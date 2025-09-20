import os
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

load_dotenv()

DEBUG_LOGS = os.getenv("DEBUG_LOGS", "false").lower() == "true"

# Load environment variables
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Check for required environment variables
if not ELEVENLABS_API_KEY or not ELEVENLABS_AGENT_ID:
    raise ValueError("Missing required ElevenLabs environment variables")

app = FastAPI(title="Twilio-ElevenLabs Integration Server")

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
                print(f"📋 Custom parameters received: {custom_parameters}")
                print(f"Call parameters - Language: {lang}, Year: {year}")

                # Get era-specific configuration
                session_vars = get_era_session_variables(year, lang)
                
                print(f"Era configuration: {session_vars['era_name']} ({session_vars['time_period']})")
                print(f"Era expressions: {session_vars['expression_1']}, {session_vars['expression_2']}, {session_vars['expression_3']}")

                # Initialize the conversation
                try:
                    # Check if we have era-specific agent IDs (environment variables)
                    era_agent_id = os.getenv(f"ELEVENLABS_AGENT_ID_{session_vars['era_name'].upper()}")
                    agent_id_to_use = era_agent_id if era_agent_id else ELEVENLABS_AGENT_ID
                    
                    print(f"Using agent ID: {agent_id_to_use} (era-specific: {bool(era_agent_id)})")
                    
                    # Create dynamic variables for the agent's system prompt (exclude voice_settings)
                    dynamic_vars = {k: v for k, v in session_vars.items() if k != 'voice_settings'}
                    
                    # Create conversation config override for voice settings
                    voice_settings = session_vars['voice_settings']
                    
                    # Use the official ElevenLabs documentation structure
                    conversation_override = {
                        "tts": {
                            # Based on official docs: individual parameters at tts level
                            "stability": voice_settings.get("stability"),
                            "similarity_boost": voice_settings.get("similarity_boost"), 
                            "style": voice_settings.get("style"),
                            "speed": voice_settings.get("speed")  # Fixed: speed not voice_speed
                        }
                    }
                    
                    print(f"🔍 Dynamic variables: {dynamic_vars}")
                    print(f"🔧 Voice settings from era config: {voice_settings}")
                    print(f"📡 Conversation override structure: {json.dumps(conversation_override, indent=2)}")
                    
                    # Try with both dynamic variables and conversation overrides
                    try:
                        # Create conversation configuration with dynamic variables and overrides
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
                            callback_agent_response=lambda text: print(f"Agent ({session_vars['era_name']}): {text}"),
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
                                callback_agent_response=lambda text: print(f"Agent (no voice override): {text}"),
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
                                callback_agent_response=lambda text: print(f"Agent (basic): {text}"),
                                callback_user_transcript=lambda text: print(f"User: {text}"),
                            )

                    # Start the conversation session
                    conversation.start_session()
                    
                    print(f"ElevenLabs conversation started successfully")
                    print(f"Era: {session_vars['era_name']} | Language: {lang} | Year: {year}")
                    print(f"Dynamic variables passed to agent for era context customization")
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