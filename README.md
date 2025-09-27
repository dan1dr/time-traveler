# 🕰️ Time Traveler Agent

An AI-powered time traveler that calls you from any historical era! Using ElevenLabs Conversational AI and Twilio, this agent embodies characters from Ancient Times to the Far Future (5000+ AD) with era-specific personalities, expressions, and voice characteristics.

## 🌟 What Makes This Project Special

- **🎭 17 Historical Eras**: From Late Bronze Age (1500 BC) to Far Future (3000+ AD) with authentic personalities
- **🌍 Bilingual Immersion**: Complete English/Spanish support with era-specific expressions
- **🎨 Beautiful UI**: Modern, responsive frontend with stunning animations and user experience
- **🔊 Real-Time Audio**: Seamless Twilio ↔ ElevenLabs integration with optimized audio conversion
- **🎲 Smart Randomization**: Voice and agent selection with character consistency
- **🚀 Production Ready**: Complete deployment infrastructure with comprehensive documentation
- **🧪 Bulletproof Testing**: 100% test coverage of critical paths with robust error handling

### 🎯 Technical Excellence
- **WebSocket Mastery**: Real-time audio streaming with Twilio Media Streams
- **Era Intelligence**: Dynamic variable injection for authentic historical context
- **Voice Adaptation**: Era-specific voice characteristics (speed, stability, style)
- **Error Resilience**: Comprehensive fallback systems and graceful degradation
- **Developer Experience**: Complete setup guides, testing infrastructure, and deployment automation

### 🏗️ Architecture Highlights
- **Modular Design**: Clean separation between server logic, shared modules, and tests
- **Type Safety**: Python dataclasses for era configuration with validation  
- **Randomization**: Language-based voice selection + personality-based agent selection
- **Character Consistency**: Voice metadata ensures character-voice alignment
- **Immersive Experience**: Era-specific first messages and voice settings
- **Testing**: 37 unit tests covering all core logic with 100% coverage of critical paths
- **Poetry Management**: Root-level dependency management for easy testing and CI/CD

## ✨ Features

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
| -1500 to -800 | Late Bronze-Early Iron | "By decree of great kings..." | 1.05 (ceremonial) |
| -800 to 0 | Classical Antiquity | "By Zeus!" | 1.1 (oratory) |
| 0 to 500 | Roman Empire | "By the will of the Senate..." | 1.05 (imperial) |
| 500 to 1000 | Early Medieval | "God guard us on these roads..." | 0.98 (monastic) |
| 1000 to 1300 | High Medieval | "By my troth!" | 1.0 (dignified) |
| 1300 to 1400 | Late Medieval | "In these troubled years..." | 0.98 (reflective) |
| 1400 to 1600 | Renaissance | "What a marvel of nature!" | 1.1 (artistic) |
| 1600 to 1750 | Baroque | "Most gracious indeed!" | 1.0 (refined) |
| 1750 to 1900 | Industrial | "What progress we have made!" | 1.15 (energetic) |
| 1900 to 1945 | Modernism & World Wars | "The old world cracks..." | 1.08 (urgent) |
| 1945 to 1991 | Cold War | "Across the wire, signals..." | 1.05 (tense) |
| 1991 to 2008 | Globalization & Early Internet | "Dial in—we're logging on..." | 1.12 (optimistic) |
| 2008 to 2030 | Mobile, Social & Cloud | "Push the update—everyone's here..." | 1.15 (fast-paced) |
| 2030 to 2050 | AI Renaissance | "The neural networks whisper..." | 1.1 (precise) |
| 2050 to 2200 | Interplanetary | "By the rings of Saturn!" | 1.0 (cosmic) |
| 2200 to 2500 | Transcendent | "Through the quantum foam..." | 0.95 (ethereal) |
| 2500 to 3000+ | Far Future | "In the symphony of galactic thoughts..." | 0.9 (profound) |

## 🔧 Configuration

### Environment Variables

**Backend (`apps/server/.env`)**
```bash
# ElevenLabs Configuration
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_AGENT_ID_1=agent_...
ELEVENLABS_AGENT_ID_2=agent_...  # Optional
ELEVENLABS_AGENT_ID_3=agent_...  # Optional

# Twilio Configuration
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...

# CORS and Debug
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app
DEBUG_LOGS=true
```

**Frontend (`apps/web/.env.local`)**
```bash
NEXT_PUBLIC_BACKEND_URL=https://your-railway-app.railway.app
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