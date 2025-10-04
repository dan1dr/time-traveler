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
- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **Rate Limiting**: Built-in sliding window rate limiting (5 calls/5min per token)
- **Type Safety**: Python dataclasses for era configuration with validation  
- **Randomization**: Language-based voice selection + personality-based agent selection
- **Character Consistency**: Voice metadata ensures character-voice alignment
- **Immersive Experience**: Era-specific first messages and voice settings
- **Testing**: 49 unit tests covering all core logic with comprehensive coverage
- **Poetry Management**: Root-level dependency management for easy testing and CI/CD

## ✨ Features

- **📞 Live Phone Calls**: Real-time conversations via Twilio integration
- **🧠 Dynamic Context**: ElevenLabs agents receive era-specific prompts and expressions
- **🔧 JSON API**: Simple REST API for initiating calls with `{to, lang, year}` parameters
- **🔐 JWT Authentication**: Secure token-based authentication for all API endpoints
- **⚡ Rate Limiting**: Built-in protection against abuse with configurable limits
- **📊 Status Monitoring**: Real-time rate limit status and call monitoring endpoints

## 🔄 How It Works

The system delivers an **outbound voice experience**: a visitor submits a form (phone, language, year) and immediately receives a call. On pickup, a **live ElevenLabs Agent** converses naturally with era-flavored style.

### Complete Call Flow

```mermaid
sequenceDiagram
  autonumber
  participant UI as Your UI (form/button)
  participant API as FastAPI Server
  participant Twilio as Twilio Voice (PSTN)
  participant WS as /outbound-media-stream (WebSocket)
  participant EL as ElevenLabs Conversation

  UI->>API: POST /outbound-call (to=+34...)
  API->>Twilio: REST calls.create(from, to, url=/outbound-call-twiml)
  Note right of Twilio: Places the phone call to the user

  Twilio->>API: GET/POST /outbound-call-twiml
  API-->>Twilio: TwiML Connect Stream url

  Twilio->>WS: WebSocket CONNECT
  WS-->>Twilio: 101 Switching Protocols

  Twilio->>WS: event start with streamSid and callSid
  WS->>EL: conversation.start_session(audio_interface)

  loop Realtime audio (caller to agent)
    Twilio->>WS: event media with base64 payload
    WS->>WS: decode and resample audio
    WS->>EL: input_callback(PCM16 16k)
    EL-->>WS: agent computes reply
  end

  loop Realtime audio (agent to caller)
    EL-->>WS: output(PCM16 16k)
    WS->>WS: base64 encode
    WS-->>Twilio: event media with payload
    Note right of Twilio: Plays audio to the caller
  end

  Twilio->>WS: event stop
  WS->>EL: end_session and cleanup
  WS-->>Twilio: socket closes
```

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

### 3. Get JWT Token
```bash
# Get authentication token
curl -X POST https://YOUR_NGROK_URL/auth/login
```

### 4. Make a Call
```bash
# Use the token from step 3
curl -X POST https://YOUR_NGROK_URL/outbound-call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
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

# JWT Authentication
JWT_SECRET=your_secure_jwt_secret_here
JWT_EXPIRATION_HOURS=24

# Rate Limiting (Optional - defaults shown)
RATE_LIMIT_CALLS=5
RATE_LIMIT_WINDOW_MINUTES=5

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

## 🔐 JWT Authentication

The API uses JWT (JSON Web Tokens) for secure authentication. All endpoints require a valid token.

### Generate JWT Secret
```bash
# Generate a secure secret for your .env file
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Authentication Flow
1. **Get Token**: `POST /auth/login` - Returns JWT token
2. **Use Token**: Include `Authorization: Bearer TOKEN` in API calls
3. **Refresh Token**: `POST /auth/refresh` - Get new token before expiration
4. **Verify Token**: `GET /auth/verify` - Check if token is valid

### Example Usage
```bash
# 1. Get token
TOKEN=$(curl -s -X POST https://your-api.com/auth/login | jq -r '.token')

# 2. Check rate limit status (optional)
curl -X GET https://your-api.com/rate-limit/status \
  -H "Authorization: Bearer $TOKEN"

# 3. Make authenticated call
curl -X POST https://your-api.com/outbound-call \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"to":"+1234567890","lang":"en","year":1350}'
```

### Rate Limiting
The API includes built-in rate limiting to prevent abuse:
- **Default**: 5 calls per 5-minute window per token
- **Configurable**: Set `RATE_LIMIT_CALLS` and `RATE_LIMIT_WINDOW_MINUTES` in environment
- **Sliding Window**: Uses a sliding window approach for fair rate limiting
- **Status Endpoint**: Check current rate limit status with `GET /rate-limit/status`
- **Error Response**: Returns HTTP 429 with detailed rate limit information when exceeded

## 📡 API Endpoints

### Authentication
- `POST /auth/login` - Get JWT token
- `POST /auth/refresh` - Refresh existing token
- `GET /auth/verify` - Verify token validity

### Core Functionality
- `POST /outbound-call` - Initiate time traveler call (requires auth)
- `GET /outbound-call-twiml` - TwiML for Twilio webhook
- `WS /outbound-media-stream` - WebSocket for real-time audio

### Monitoring & Status
- `GET /rate-limit/status` - Check current rate limit status (requires auth)
- `GET /call-status/{callSid}` - Get call status (requires auth)
- `POST /end-call/{callSid}` - End active call (requires auth)
- `GET /config` - Get server configuration
- `GET /health` - Health check endpoint

## 📁 Project Structure

### Complete Repository Layout

```
time-traveler/
├─ apps/
│  ├─ web/                      # Next.js (Vercel) UI
│  │  ├─ src/app/              # Next.js app directory
│  │  ├─ src/components/        # React components
│  │  └─ package.json          # Frontend dependencies
│  └─ server/                   # FastAPI backend with modular architecture
│     ├─ main.py               # API endpoints & orchestration
│     ├─ auth.py               # JWT authentication & user management
│     ├─ rate_limiting.py      # Rate limiting logic & storage
│     ├─ twilio_audio.py       # Twilio audio bridge & WebSocket handler
│     ├─ era_config.py         # Era definitions and voice settings
│     ├─ errors.py             # Error handling
│     └─ pyproject.toml        # Server dependencies (Poetry)
├─ apps/server/shared_py/       # Python shared modules
│  ├─ data/                     # JSON data files
│  │  ├─ voices.json            # Voice IDs with gender/age metadata
│  │  ├─ agents.json            # Agent personalities
│  │  └─ first_messages.json    # Era-specific greetings
│  ├─ voice_manager.py          # Voice randomization logic
│  ├─ agent_manager.py          # Agent randomization logic
│  └─ first_message_manager.py  # First message selection
├─ tests/                      # Unit tests (pytest)
│  ├─ test_voice_manager.py    # Voice manager tests
│  ├─ test_agent_manager.py    # Agent manager tests
│  ├─ test_era_config.py       # Era configuration tests
│  ├─ test_rate_limiting.py    # Rate limiting tests
│  └─ conftest.py              # Test fixtures and setup
├─ infra/
│  ├─ deployment/              # Deployment guides (Vercel + Railway)
│  │  └─ README.md             # Complete deployment guide
│  ├─ twilio/                  # Twilio setup and configuration
│  │  └─ README.md             # Twilio voice setup guide
│  └─ docker/                  # Dockerfiles/compose (optional)
├─ scripts/                    # Dev helpers (no app logic)
├─ pyproject.toml              # Root Poetry project for testing
├─ poetry.lock                 # Root dependency lock file
├─ README.md                   # This file
└─ package.json                # JS workspaces root (web + shared-ts)
```

### Backend Architecture
The server follows a **modular architecture** for maintainability and scalability:

```
apps/server/
├── main.py              # API endpoints & orchestration
├── auth.py              # JWT authentication & user management
├── rate_limiting.py     # Rate limiting logic & storage
├── twilio_audio.py      # Audio interface for Twilio Media Streams
├── era_config.py        # Era definitions and voice settings
├── errors.py            # Error handling
└── shared_py/           # Shared modules
    ├── voice_manager.py
    ├── agent_manager.py
    └── first_message_manager.py
```

### Module Responsibilities
- **`main.py`** - API endpoint definitions, request/response handling, business logic orchestration
- **`auth.py`** - JWT token creation/validation, user authentication, session management
- **`rate_limiting.py`** - Rate limit checking/enforcement, token-based limiting, memory management
- **`twilio_audio.py`** - Twilio Media Streams integration, audio conversion
- **`era_config.py`** - Historical era definitions, voice settings, expressions
- **`shared_py/`** - Reusable modules for voice/agent management and randomization

### Architecture Benefits

The modular design provides several advantages:

- **✅ Single Responsibility**: Each module has one clear purpose
- **✅ Testability**: Modules can be tested independently with focused unit tests
- **✅ Reusability**: Auth and rate limiting modules can be used by other services
- **✅ Maintainability**: Changes to one module don't affect others
- **✅ Scalability**: Modules can be moved to separate services as the project grows

### Testing Philosophy

Each module can be tested independently with focused unit tests:

```python
# Test auth module
from auth import create_jwt_token, validate_jwt_token

# Test rate limiting module  
from rate_limiting import check_rate_limit, get_rate_limit_config

# Test era configuration
from era_config import get_era_config, get_era_session_variables
```

The project includes **49 unit tests** covering all core logic with comprehensive coverage of edge cases and error conditions.

## 🎯 Example Conversations

**Medieval Knight (1350, Spanish):**
> "¡Por mi fe! En estos tiempos oscuros, ¿qué extraña magia es esa que te permite hablar conmigo a través del tiempo?"

**1970s Hippie (1970, English):**
> "Far out, man! The space age is upon us and you're like, calling from the future? That's totally groovy!"

**AI Renaissance (2035, English):**
> "The neural networks whisper such wisdom... My AI companion suggests we consider how your primitive devices evolved into our symbiotic consciousness."

## 📊 Performance & Latency Testing

Performance metrics and latency testing results are available in [`apps/server/metrics/`](apps/server/metrics/README.md), including:

- **Setup latency**: WebSocket connection to first audible audio
- **Turn-by-turn metrics**: User speech → agent response timing
- **Model comparison**: LLM and TTS performance across different agents
- **Audio streaming**: Chunk cadence and quality metrics

See the metrics folder for detailed test setup, methodology, and results.

## 🚀 Future Improvements

1. **Dependency Injection**: Use FastAPI's dependency injection more extensively
2. **Configuration Management**: Centralized config with validation
3. **Database Layer**: Separate data access layer
4. **Service Layer**: Business logic in dedicated services
5. **API Versioning**: Separate modules for different API versions

Built with ❤️ using ElevenLabs, Twilio, and FastAPI.