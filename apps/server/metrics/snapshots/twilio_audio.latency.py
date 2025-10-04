import asyncio
import base64
import json
from fastapi import WebSocket
from elevenlabs.conversational_ai.conversation import AudioInterface
from starlette.websockets import WebSocketDisconnect, WebSocketState
import audioop 
import os
import time

class TwilioAudioInterface(AudioInterface):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.input_callback = None
        self.stream_id = None
        self.loop = asyncio.get_event_loop()
        self.frames = 0
        self.debug_logs = os.getenv("DEBUG_LOGS", "false").lower() == "true"
        # Persistent resampling state to avoid discontinuities between frames
        self._ratecv_state = None
        # Metrics
        self.first_out_sent_at_ms = None
        self.prev_out_sent_at_ms = None
        self.out_intervals_ms = []
        self.last_in_media_at_ms = None
        self.min_round_trip_ms = None

    def start(self, input_callback):
        self.input_callback = input_callback

    def stop(self):
        self.input_callback = None
        self.stream_id = None
        # Reset resampler state on stop
        self._ratecv_state = None
        # Do not reset metrics here; they will be read after stop

    def output(self, audio: bytes):
        """
        This method should return quickly and not block the calling thread.
        """
        now_ms = int(time.monotonic() * 1000)
        if self.first_out_sent_at_ms is None:
            self.first_out_sent_at_ms = now_ms
        if self.prev_out_sent_at_ms is not None:
            self.out_intervals_ms.append(now_ms - self.prev_out_sent_at_ms)
        self.prev_out_sent_at_ms = now_ms

        # Update rough round-trip: time since last inbound user frame
        if self.last_in_media_at_ms is not None:
            rt = now_ms - self.last_in_media_at_ms
            if rt >= 0:
                if self.min_round_trip_ms is None or rt < self.min_round_trip_ms:
                    self.min_round_trip_ms = rt

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
            # Reset resampler state at the beginning of a stream
            self._ratecv_state = None
        elif event_type == "media" and self.input_callback:
            self.frames += 1
            mu = base64.b64decode(message["media"]["payload"])  # μ-law 8k
            pcm = self._mulaw8k_to_pcm16(mu, target_rate=16000) # s16le 16k
            try:
                self.input_callback(pcm)
            except Exception:
                # Swallow input callback errors to avoid breaking the stream; EL will handle
                pass
            # Record inbound timing
            try:
                self.last_in_media_at_ms = int(time.monotonic() * 1000)
            except Exception:
                pass
            if self.debug_logs and self.frames % 50 == 0:
                print(f"Received {self.frames} media frames")

    def export_metrics(self) -> dict:
        """Return collected audio-side metrics for this stream."""
        return {
            "first_out_ms": self.first_out_sent_at_ms,
            "avg_out_interval_ms": (sum(self.out_intervals_ms) / len(self.out_intervals_ms)) if self.out_intervals_ms else None,
            "p95_out_interval_ms": (sorted(self.out_intervals_ms)[int(len(self.out_intervals_ms)*0.95)] if self.out_intervals_ms else None),
            "min_round_trip_ms": self.min_round_trip_ms,
            "out_intervals_count": len(self.out_intervals_ms),
        }

            

