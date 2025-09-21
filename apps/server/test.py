from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ConversationInitiationData

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 1) Verifica que el voice_id existe en TU workspace
client.voices.get_settings("VWQuOfcP7ILB48IXXGXE")  # debe NO lanzar excepción

# 2) Arranca una sesión vacía con solo el override de voice_id
cfg = ConversationInitiationData(
    conversation_config_override={"tts": {"voice_id": "VWQuOfcP7ILB48IXXGXE"}}
)
conv = Conversation(client=client, agent_id=ELEVENLABS_AGENT_ID, config=cfg, requires_auth=True)
conv.start_session()
conv.end_session(); conv.wait_for_session_end()
