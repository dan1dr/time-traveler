## Latency Test — Time-Traveler Voice Agent (Twilio + ElevenLabs)

### Test Setup
- **Environment**: Local development server (WebSocket media stream)
- **Telephony**: Twilio trial account with default trial settings
- **Region**: Fixed/defined Twilio region (constant across runs)
- **Call path**: US Twilio number → Spanish destination
- **Agent / Speech**: ElevenLabs — Flash v2.5, Spanish language, multiple voices
- **LLM prompt & params**: System prompt with dynamic variables; temperature = 0.5
- **LLMs compared (agent mapping)**:
  - **Model 1**: Gemini Flash 2.0
  - **Model 2**: Claude 3 Haiku
  - **Model 3**: GPT-OSS 120B
- **Runs**: 3 calls per model (9 total)

### Method (metrics captured)
- **Startup**: `setup_ms`, `first_audio_ms`, `first_sentence_delta_ms`
- **Conversation span**: `last_agent_text_delta_ms`, `sentences_spoken`
- **Audio pacing**: `audio.avg_out_interval_ms`, `audio.p95_out_interval_ms` (gaps between outbound audio chunks; includes silences)
- **Model timings (from ElevenLabs)**: LLM time to first sentence and TTS time aggregated per call; derived:
  - `llm_plus_tts_ms = avg_llm_ms + avg_tts_ms`
  - `setup_overhead_ms = setup_ms − llm_plus_tts_ms`

### Results (simple)
- **First audible audio**: ~1.5 s end-to-end
  - Decomposed as LLM+TTS ~1.25–1.30 s + ~0.27–0.37 s transport/boot/buffering
- **Between-turn pacing (avg & p95 gaps)**: very similar across all three; only small deltas
  - **Claude 3 Haiku**: slightly tighter average/tail gaps
  - **GPT-OSS 120B**: slightly lower startup overhead (earliest first sound)
  - **Gemini Flash 2.0**: modestly larger average gap
- **Conversation span & verbosity**: similar (≈3–4 sentences per call)
- **Bottom line**: No meaningful performance separation with just 3 calls per model; differences are minor and not statistically significant for this sample
