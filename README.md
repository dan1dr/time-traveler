# 🧞‍♂️ Time Traveler Agent

The Time Traveler lets you receive a real phone call from any point in history — from the Bronze Age to the year 3000. Each voice you hear is alive in its own era, speaking naturally in English or Spanish, shaped by the beliefs, sounds, and tools of their time.

Built with ElevenLabs, it mixes historical storytelling with real-time audio synthesis — creating an illusion so vivid it feels like you’re truly speaking across centuries.

## Demo

[![Watch the demo](https://img.youtube.com/vi/S5TnaWNuPHw/hqdefault.jpg)](https://youtu.be/S5TnaWNuPHw?si=93NcJdDhWSL7WfAX "Watch the demo on YouTube")

## About this project

- **17 Historical Eras**: From Late Bronze Age (1500 BC) to Far Future (3000+ AD) with authentic personalities
- **Multiple agents & personalities**: Several ElevenLabs agents with distinct styles; the system selects and adapts personality per era
- **Diverse voices**: Language-specific voice pools with gender/age metadata; voices are randomized while voice settings adapt to the era
- **Bilingual Immersion**: Complete English/Spanish support with era-specific expressions
- **Beautiful UI**: Modern, responsive frontend with stunning animations and user experience
- **Real-Time Audio**: Seamless Twilio ↔ ElevenLabs integration with optimized audio conversion
- **Smart Randomization**: Voice and agent selection with character consistency
- **Production Ready**: Complete deployment infrastructure with comprehensive documentation


## Features

- **Live Phone Calls**: Real-time conversations via Twilio integration
- **Dynamic Context**: ElevenLabs agents receive era-specific prompts and expressions
- **JSON API**: Simple REST API for initiating calls with `{to, lang, year}` parameters
- **JWT Authentication**: Secure token-based authentication for all API endpoints
- **Rate Limiting**: Built-in protection against abuse with configurable limits
- **Status Monitoring**: Real-time rate limit status and call monitoring endpoints

## How It Works

The system delivers an **outbound voice experience**: a visitor submits a form (phone, language, year) and immediately receives a call. On pickup, a **live ElevenLabs Agent** converses naturally with era-flavored style.

 



## 🚀 Quick Start

### Prerequisites
1. **ElevenLabs Agent Setup**: Create and configure your conversational agents → [apps/server/README.md](apps/server/README.md)
2. **Twilio Integration**: Set up Twilio phone number and webhooks → [infra/twilio/README.md](infra/twilio/README.md)
3. **Environment Variables**: Configure `.env` files (see Configuration section below)

### Local Development

#### 1. Start the Backend
```bash
cd apps/server
# Install dependencies with Poetry (creates/uses a virtualenv)
poetry install

# Run the API
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Start ngrok (separate terminal)
```bash
ngrok http 8000
```

#### 3. Start the Frontend (localhost)
```bash
cd apps/web
pnpm install  # or: npm install / yarn

# Create .env.local with your ngrok URL
echo "NEXT_PUBLIC_BACKEND_URL=https://YOUR_NGROK_URL" > .env.local

# Run dev server
pnpm dev  # or: npm run dev / yarn dev
# Open http://localhost:3000
```

#### 4. Test with cURL (optional)
```bash
# Get authentication token
TOKEN=$(curl -s -X POST https://YOUR_NGROK_URL/auth/login | jq -r '.token')

# Make a test call
curl -X POST https://YOUR_NGROK_URL/outbound-call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "to": "+1234567890",
    "lang": "en",
    "year": 1350
  }'
```

### Production Deployment
- **Frontend (Vercel)**: See [infra/deployment/README.md](infra/deployment/README.md) for complete Vercel deployment guide
- **Backend (Railway)**: Detailed in the same deployment guide
- **Complete Instructions**: [apps/server/README.md](apps/server/README.md) and [apps/web/README.md](apps/web/README.md)

 
## Configuration

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

## JWT Authentication

The API uses JWT (JSON Web Tokens) for secure authentication. All endpoints require a valid token.

For detailed examples (including cURL snippets), see the backend guide:
- [apps/server/README.md](apps/server/README.md)

## API Endpoints

### Public
- `GET /` - Root
- `GET /health` - Health check

### Authentication
- `POST /auth/login` - Get JWT token
- `POST /auth/refresh` - Refresh existing token
- `GET /auth/verify` - Verify token validity

### Core Functionality
- `OPTIONS /outbound-call` - CORS preflight handler
- `POST /outbound-call` - Initiate time traveler call (requires auth)
- `GET /outbound-call-twiml` - TwiML for Twilio webhook
- `POST /outbound-call-twiml` - TwiML webhook (Twilio may POST)
- `WS /outbound-media-stream` - WebSocket for real-time audio

### Monitoring & Status
- `GET /rate-limit/status` - Check current rate limit status (requires auth)
- `GET /call-status/{callSid}` - Get call status (requires auth)
- `POST /end-call/{callSid}` - End active call (requires auth)
- `GET /config` - Get server configuration (debug)

## Project Structure

### Complete Repository Layout

```
time-traveler/
├─ apps/
│  ├─ web/                      # Next.js (Vercel) UI
│  │  ├─ src/app/               # Next.js app directory
│  │  ├─ src/components/        # React components
│  │  └─ package.json           # Frontend dependencies
│  └─ server/                   # FastAPI backend with modular architecture
│     ├─ main.py                # API endpoints & orchestration
│     ├─ auth.py                # JWT authentication & user management
│     ├─ rate_limiting.py       # Rate limiting logic & storage
│     ├─ twilio_audio.py        # Twilio audio bridge & WebSocket handler
│     ├─ era_config.py          # Era definitions and voice settings
│     ├─ errors.py              # Error handling
│     └─ pyproject.toml         # Server dependencies (Poetry)
├─ apps/server/shared_py/       # Python shared modules
│  ├─ data/                     # JSON data files (voices, agents, first messages)
│  ├─ voice_manager.py          # Voice randomization logic
│  ├─ agent_manager.py          # Agent randomization logic
│  └─ first_message_manager.py  # First message selection
├─ apps/server/metrics/         # Latency metrics, snapshots, and UI config
├─ tests/                       # Unit tests (pytest)
│  ├─ test_voice_manager.py
│  ├─ test_agent_manager.py
│  ├─ test_era_config.py
│  ├─ test_rate_limiting.py
│  └─ conftest.py
├─ infra/
│  ├─ deployment/               # Deployment guides (Vercel + Railway)
│  │  └─ README.md
│  └─ twilio/                   # Twilio setup and configuration
│     └─ README.md
├─ pyproject.toml               # Root Poetry project for testing
├─ poetry.lock                  # Root dependency lock file
├─ README.md                    # Root documentation (you are here)
└─ package.json                 # JS workspaces root (web + shared-ts)
```

<!-- Backend architecture overview intentionally omitted; see apps/server/README.md for full details. -->

### Module Responsibilities
- **`main.py`** - API endpoint definitions, request/response handling, business logic orchestration
- **`auth.py`** - JWT token creation/validation, user authentication, session management
- **`rate_limiting.py`** - Rate limit checking/enforcement, token-based limiting, memory management
- **`twilio_audio.py`** - Twilio Media Streams integration, audio conversion
- **`era_config.py`** - Historical era definitions, voice settings, expressions
- **`shared_py/`** - Reusable modules for voice/agent management and randomization

### Architecture Benefits

The modular design provides several advantages:

- **Single Responsibility**: Each module has one clear purpose
- **Testability**: Modules can be tested independently with focused unit tests
- **Reusability**: Auth and rate limiting modules can be used by other services
- **Maintainability**: Changes to one module don't affect others
- **Scalability**: Modules can be moved to separate services as the project grows

### Testing Philosophy

Run tests with Poetry at the repo root:
```bash
poetry run pytest -q
```
Or run a specific module, e.g.:
```bash
poetry run pytest tests/test_rate_limiting.py -q
```

## Example Conversations

**Medieval Knight (1350, Spanish):**
> "¡Por mi fe! En estos tiempos oscuros, ¿qué extraña magia es esa que te permite hablar conmigo a través del tiempo?"

**1970s Hippie (1970, English):**
> "Far out, man! The space age is upon us and you're like, calling from the future? That's totally groovy!"

**AI Renaissance (2035, English):**
> "The neural networks whisper such wisdom... My AI companion suggests we consider how your primitive devices evolved into our symbiotic consciousness."

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

## Performance & Latency Testing

Performance metrics and latency testing results are available in [`apps/server/metrics/`](apps/server/metrics/README.md), including:

- **Setup latency**: WebSocket connection to first audible audio
- **Turn-by-turn metrics**: User speech → agent response timing
- **Model comparison**: LLM and TTS performance across different agents
- **Audio streaming**: Chunk cadence and quality metrics

See the metrics folder for detailed test setup, methodology, and results.

## Future Improvements

1. **Extended agent memory**: Persist conversational memory in a database to recall prior calls and tailor responses
2. **Advanced rate limiting & monitoring**: More granular quotas, per-route policies, dashboards, and deeper test coverage
3. **Live tool access for the agent**: Controlled tools (search, retrieval, functions) with auditing and safety rails

Built with ❤️ using ElevenLabs and Twilio.