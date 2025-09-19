import asyncio
import base64
import json
from fastapi import WebSocket
# from elevenlabs.conversational_ai.audio_interface import AudioInterface
from elevenlabs.conversational_ai.conversation import AudioInterface
from starlette.websockets import WebSocketDisconnect, WebSocketState
import audioop 
import os

class TwilioAudioInterface(AudioInterface):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.input_callback = None
        self.stream_id = None
        self.loop = asyncio.get_event_loop()
        self.frames = 0
        self.debug_logs = os.getenv("DEBUG_LOGS", "false").lower() == "true"

    def start(self, input_callback):
        self.input_callback = input_callback

    def stop(self):
        self.input_callback = None
        self.stream_id = None

    def output(self, audio: bytes):
        """
        This method should return quickly and not block the calling thread.
        """
        asyncio.run_coroutine_threadsafe(self.send_audio_to_twilio(audio), self.loop)

    def interrupt(self):
        asyncio.run_coroutine_threadsafe(self.send_clear_message_to_twilio(), self.loop)
    
 
    def _mulaw8k_to_pcm16(self, mu_bytes: bytes, target_rate=16000) -> bytes:
        """
        Twilio sends μ-law (G.711) @ 8kHz.
        Convert μ-law -> linear PCM s16le, and (optionally) upsample 8k -> 16k.
        """
        # μ-law (1 byte/sample) -> linear PCM s16le (2 bytes/sample)
        lin8k = audioop.ulaw2lin(mu_bytes, 2)
        if target_rate and target_rate != 8000:
            lin16k, _ = audioop.ratecv(lin8k, 2, 1, 8000, target_rate, None)
            return lin16k
        return lin8k

    async def send_audio_to_twilio(self, audio: bytes):
        if self.stream_id:
            audio_payload = base64.b64encode(audio).decode('utf-8')
            audio_delta = {
                "event": "media",
                "streamSid": self.stream_id,
                "media": {
                    "payload": audio_payload
                }
            }
            try:
                if self.websocket.application_state == WebSocketState.CONNECTED:
                    await self.websocket.send_text(json.dumps(audio_delta))
            except (WebSocketDisconnect, RuntimeError):
                pass

    async def send_clear_message_to_twilio(self):
        if self.stream_id:
            clear_message = {"event": "clear", "streamSid": self.stream_id}
            try:
                if self.websocket.application_state == WebSocketState.CONNECTED:
                    await self.websocket.send_text(json.dumps(clear_message))
            except (WebSocketDisconnect, RuntimeError):
                pass



    async def handle_twilio_message(self, message: dict):
        event_type = message.get("event")
        if event_type == "start":
            self.stream_id = message["start"]["streamSid"]
        elif event_type == "media" and self.input_callback:
            self.frames += 1
            mu = base64.b64decode(message["media"]["payload"])  # μ-law 8k
            pcm = self._mulaw8k_to_pcm16(mu, target_rate=16000) # s16le 16k
            self.input_callback(pcm)
            if self.debug_logs and self.frames % 50 == 0:
                print(f"Received {self.frames} media frames")

            

