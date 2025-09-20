# 🕰️ Time Traveler Agent

An AI-powered time traveler that calls you from any historical era! Using ElevenLabs Conversational AI and Twilio, this agent embodies characters from Ancient Times to the Far Future (5000+ AD) with era-specific personalities, expressions, and voice characteristics.

## ✨ Features

- **🎭 12 Historical Eras**: From Ancient civilizations to Far Future galactic consciousness
- **🌍 Bilingual Support**: English and Spanish expressions for each era
- **🎛️ Voice Adaptation**: Era-specific voice speed, stability, and style settings
- **📞 Live Phone Calls**: Real-time conversations via Twilio integration
- **🧠 Dynamic Context**: ElevenLabs agents receive era-specific prompts and expressions
- **🔧 JSON API**: Simple REST API for initiating calls with `{to, lang, year}` parameters

## 🚀 Quick Start

### 1. Start the Server
```bash
cd apps/server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start ngrok (separate terminal)
```bash
ngrok http 8000
```

### 3. Make a Call
```bash
curl -X POST https://YOUR_NGROK_URL/outbound-call \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "lang": "en",
    "year": 1350
  }'
```

## 🎭 Available Eras

| Year Range | Era | Example Expression | Voice Speed |
|------------|-----|-------------------|-------------|
| 0-500 | Ancient Times | "By the gods!" | 0.9 (wisdom) |
| 500-1500 | Medieval | "By my troth!" | 1.0 (normal) |
| 1400-1600 | Renaissance | "What a marvel!" | 1.1 (artistic) |
| 1600-1750 | Baroque | "Most gracious!" | 0.95 (refined) |
| 1750-1900 | Industrial | "What progress!" | 1.15 (energetic) |
| 1900-1950 | Early Modern | "What a time to be alive!" | 1.2 (fast-paced) |
| 1950-2000 | Mid-Late 20th | "Far out, man!" | 1.2 (groovy) |
| 2000-2030 | Contemporary | "Amazing how connected..." | 1.1 (quick) |
| 2030-2050 | AI Renaissance | "Neural networks whisper..." | 1.0 (measured) |
| 2050-2200 | Interplanetary | "By the rings of Saturn!" | 0.85 (cosmic) |
| 2200-2500 | Transcendent | "Quantum foam of consciousness..." | 0.7 (ethereal) |
| 2500+ | Far Future | "Symphony of galactic thoughts..." | 0.7 (profound) |

## 🔧 Configuration

### Environment Variables
```bash
ELEVENLABS_API_KEY=your_key
ELEVENLABS_AGENT_ID=your_agent_id
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number
```

### ElevenLabs Agent Setup
Configure your agent with dynamic variables in the system prompt:
```
You are a time traveler from the year {{era_year}} during the {{time_period}}.
LANGUAGE: Always respond in {{language_name}}.
PERSONALITY: Use these expressions naturally: "{{expression_1}}", "{{expression_2}}", "{{expression_3}}"
```

See `apps/server/AGENT_SETUP.md` for complete configuration guide.

## 📁 Project Structure

- **`apps/server/`** - FastAPI backend with era logic
- **`apps/server/era_config.py`** - Era definitions and voice settings
- **`apps/server/main.py`** - API endpoints and conversation handling
- **`apps/server/twilio_audio.py`** - Audio interface for Twilio Media Streams

## 🎯 Example Conversations

**Medieval Knight (1350, Spanish):**
> "¡Por mi fe! En estos tiempos oscuros, ¿qué extraña magia es esa que te permite hablar conmigo a través del tiempo?"

**1970s Hippie (1970, English):**
> "Far out, man! The space age is upon us and you're like, calling from the future? That's totally groovy!"

**AI Renaissance (2035, English):**
> "The neural networks whisper such wisdom... My AI companion suggests we consider how your primitive devices evolved into our symbiotic consciousness."

Built with ❤️ using ElevenLabs, Twilio, and FastAPI.
