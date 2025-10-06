# ElevenLabs Agent Setup Guide

This guide explains how to configure and customize ElevenLabs agents for the Time Traveler voice application, including era-specific personality and voice settings.

## Current Server Structure

```
apps/server/
├── main.py              # API endpoints & orchestration
├── auth.py              # JWT authentication & user management  
├── rate_limiting.py     # Rate limiting logic & storage
├── twilio_audio.py      # Twilio audio handling
├── era_config.py        # Era definitions and voice settings
├── errors.py            # Error handling
└── shared_py/           # Shared modules
    ├── voice_manager.py
    ├── agent_manager.py
    └── first_message_manager.py
```

## How It Works

The system uses **3 configuration files** to manage agents and voices:

1. **`.env`** - Your ElevenLabs agent IDs from the dashboard
2. **`agents.json`** - Agent names and tracking (for logging/debugging)  
3. **`voices.json`** - Voice pool configuration for each language

The system automatically adapts agent personality, expressions, and voice settings based on the historical era determined by the `year` parameter in API calls.

## Step 1: Create Agents in ElevenLabs Dashboard

1. Go to your ElevenLabs dashboard
2. Create multiple agents with different personalities
3. Copy each agent's ID

## Step 2: Configure Environment Variables

Add your agent IDs to `.env`:

```bash
# Required: At least one agent ID
ELEVENLABS_AGENT_ID_1=your_first_agent_id_here

# Optional: Add more agents for variety
ELEVENLABS_AGENT_ID_2=your_second_agent_id_here
ELEVENLABS_AGENT_ID_3=your_third_agent_id_here

# Voice pools (fallback if voices.json is empty)
ELEVENLABS_VOICES_ES=voice1,voice2,voice3
ELEVENLABS_VOICES_EN=voice1,voice2,voice3
```

**Default Behavior**: If no agents are configured, the system uses `ELEVENLABS_AGENT_ID_1`.

## Step 3: Update agents.json

Edit `shared_py/data/agents.json` to track your agents:

```json
{
  "agents": [
    {
      "name": "Time Traveler - Scholar",
      "env_var": "ELEVENLABS_AGENT_ID_1"
    },
    {
      "name": "Time Traveler - Adventurer", 
      "env_var": "ELEVENLABS_AGENT_ID_2"
    },
    {
      "name": "Time Traveler - Mystic",
      "env_var": "ELEVENLABS_AGENT_ID_3"
    }
  ]
}
```

**Purpose**: This file helps with logging and debugging. The `name` field appears in logs, and `env_var` tells the system which environment variable to use.

## Step 4: Update voices.json

Edit `shared_py/data/voices.json` to configure voice pools:

```json
{
  "spanish": [
    {
      "id": "your_spanish_voice_id_1",
      "name": "Spanish Voice 1",
      "gender": "female",
      "age_range": "young adult"
    },
    {
      "id": "your_spanish_voice_id_2", 
      "name": "Spanish Voice 2",
      "gender": "male",
      "age_range": "elderly"
    }
  ],
  "english": [
    {
      "id": "your_english_voice_id_1",
      "name": "English Voice 1", 
      "gender": "male",
      "age_range": "middle-aged"
    }
  ]
}
```

**Purpose**: The system randomly selects voices from these pools. The `gender` and `age_range` fields are used for passing the right context to the LLM about the voice characteristics, helping maintain consistency between what the agent says and how it sounds.

**⚠️ Important**: For conversational agents, any voice ID you override must be added to "My Voices" in your ElevenLabs dashboard. If the voice isn't in your voice library, the agent will fall back to its default voice.

## Step 5: Understanding Era Configuration

The system automatically maps years to historical eras and configures the agent accordingly:

### Era Mappings

| Year Range | Era | Sample Expressions |
|------------|-----|-------------------|
| **-1500 to -800** | Late Bronze–Early Iron Age | "By decree of great kings...", "Under the gaze of the sun god..." |
| **-800 to 0** | Classical Antiquity | "By Zeus!", "In the agora we debated..." |
| **0 to 500** | Roman Empire / Late Antiquity | "By the will of the Senate...", "Under the peace of the Emperor..." |
| **500 to 1000** | Early Middle Ages | "God guard us on these rough roads...", "In the cloister we preserve..." |
| **1000 to 1300** | High Middle Ages | "By my troth!", "The cathedral spires reach toward heaven..." |
| **1300 to 1400** | Late Middle Ages | "In these troubled years...", "Plague and famine test our faith..." |
| **1400 to 1600** | Renaissance | "What a marvel of nature!", "In the spirit of discovery..." |
| **1600 to 1750** | Baroque Era | "Most gracious indeed!", "In the court of the Sun King..." |
| **1750 to 1900** | Industrial Revolution | "What progress we have made!", "The age of steam and steel..." |
| **1900 to 1945** | Modernism & World Wars | "The old world cracks...", "Under dark clouds, nations march..." |
| **1945 to 1991** | Cold War | "Across the wire, signals and shadows...", "Under the atom's glare..." |
| **1991 to 2008** | Globalization & Early Internet | "Dial in—we're logging on...", "Across new markets..." |
| **2008 to 2030** | Mobile • Social • Cloud | "Push the update—everyone's already here...", "Feeds hum..." |
| **2030 to 2050** | AI Renaissance | "The neural networks whisper...", "My AI companion suggests..." |
| **2050 to 2200** | Interplanetary Era | "By the rings of Saturn!", "When I last visited the Martian colonies..." |
| **2200 to 2500** | Transcendent Age | "Through the quantum foam of consciousness...", "My distributed essence perceives..." |
| **2500+** | Far Future | "In the symphony of galactic thoughts...", "The ancient humans would call this magic..." |

### How Era Selection Works

1. **API Call**: Include `year` parameter in your API call
   ```json
   {
     "to": "+1234567890",
     "lang": "en",
     "year": 1350
   }
   ```

2. **Automatic Mapping**: System maps year to appropriate era configuration
3. **Dynamic Variables**: Era-specific expressions and context are injected into the agent's system prompt
4. **Voice Settings**: Era-appropriate voice characteristics (speed, stability, style) are applied

### Era-Specific Features

Each era includes:
- **Authentic Expressions**: 2-3 period-appropriate phrases in English and Spanish
- **Cultural Context**: Historical background for the agent's personality
- **Voice Settings**: Optimized stability, similarity, and style for the era
- **Time Period Name**: Display name for the era

## Step 6: Configure ElevenLabs Agents

In your ElevenLabs dashboard, for each agent:

### Required Settings
- **Enable Overrides**: Turn on all override options (Voice ID, System Prompt, Language, etc.)
- **System Prompt**: Use this template with dynamic variables:

```
You are a time traveler from the year {{era_year}} during the {{time_period}}.

HISTORICAL CONTEXT: {{era_context}}

LANGUAGE: Always respond in {{language_name}}.

PERSONALITY: Use these expressions naturally:
- "{{expression_1}}"
- "{{expression_2}}"  
- "{{expression_3}}"

[Add your personality-specific instructions here]

Keep responses to 3 sentences or less. Be curious about the present day.
```

**Dynamic Variables Explained**:
- `{{era_year}}` - The specific year (e.g., 1350)
- `{{time_period}}` - Era display name (e.g., "High Middle Ages")
- `{{era_context}}` - Historical background (e.g., "feudal order, chivalry, scholasticism...")
- `{{language_name}}` - Language name (e.g., "English" or "Spanish")
- `{{expression_1}}`, `{{expression_2}}`, `{{expression_3}}` - Era-appropriate phrases

## Dynamic Variables Override System

The system automatically passes these variables to your ElevenLabs agent, allowing for dynamic personality adaptation:

### Core Era Variables
- **`era_year`**: The exact year from the API call (e.g., `1350`)
- **`time_period`**: Human-readable era name (e.g., `"High Middle Ages"`)
- **`era_name`**: Technical era identifier (e.g., `"high_medieval"`)
- **`era_context`**: Historical background for the agent (e.g., `"feudal order, chivalry, scholasticism, cathedrals, town charters, crusading ethos"`)
- **`language`**: Language code (e.g., `"en"` or `"es"`)
- **`language_name`**: Full language name (e.g., `"English"` or `"Spanish"`)

### Expression Variables
- **`expression_1`**: First era-appropriate phrase (e.g., `"By my troth!"`)
- **`expression_2`**: Second era-appropriate phrase (e.g., `"The cathedral spires reach toward heaven..."`)
- **`expression_3`**: Third era-appropriate phrase (e.g., `"As true as tempered steel..."`)

### Voice Metadata Variables
- **`voice_gender`**: Gender of the selected voice (e.g., `"male"`, `"female"`)
- **`voice_age_range`**: Age range of the selected voice (e.g., `"young adult"`, `"elderly"`)

### How Variables Are Used

1. **System Prompt Injection**: Variables are injected into your agent's system prompt template
2. **Character Consistency**: Voice metadata helps the agent maintain consistency between what it says and how it sounds
3. **Era Authenticity**: Historical context and expressions make the agent speak authentically for its time period
4. **Language Adaptation**: Language variables ensure proper response language

### Example Variable Set (Medieval Era, English, Male Voice)
```json
{
  "era_year": 1350,
  "time_period": "High Middle Ages", 
  "era_name": "high_medieval",
  "era_context": "feudal order, chivalry, scholasticism, cathedrals, town charters, crusading ethos",
  "language": "en",
  "language_name": "English",
  "expression_1": "By my troth!",
  "expression_2": "The cathedral spires reach toward heaven...",
  "expression_3": "As true as tempered steel...",
  "voice_gender": "male",
  "voice_age_range": "middle-aged"
}
```

**💡 If you want to check a previous prompt template we used, see** [here](SYSTEM_PROMPT_TEMPLATE.txt). You can also change system prompts across agents to increase variability, while you can also introduce higher temperature values or even change LLM providers as I did (have fun touching those).

### Conversation Settings
- Enable barge-in
- Set response length to short (≤3 sentences)
- Enable dynamic variables

## How Randomization Works

1. **Agent Selection**: System randomly picks from `agents.json` → uses corresponding `ELEVENLABS_AGENT_ID_X`
2. **Voice Selection**: System randomly picks from `voices.json` based on language
3. **Era Configuration**: System maps year to historical era and applies appropriate settings
4. **Fallback**: If JSON files are empty, falls back to environment variables

**💡 For technical implementation details**, see [SIMPLIFIED-RANDOMIZATION.md](SIMPLIFIED-RANDOMIZATION.md)

## Example Usage Scenarios

### Medieval Knight (1350, English)
```json
{
  "to": "+1234567890",
  "lang": "en", 
  "year": 1350
}
```
**Result**: Agent speaks like a medieval knight with expressions like "By my troth!" and context about feudal order and chivalry.

### Renaissance Artist (1550, Spanish)  
```json
{
  "to": "+1234567890",
  "lang": "es",
  "year": 1550  
}
```
**Result**: Agent speaks like a Renaissance artist with expressions like "¡Qué maravilla de la naturaleza!" and context about artistic discovery.

### 1960s Hippie (1968, English)
```json
{
  "to": "+1234567890", 
  "lang": "en",
  "year": 1968
}
```
**Result**: Agent speaks like a 1960s counterculture figure with expressions about the space age and cultural revolution.

### Future AI Companion (2040, English)
```json
{
  "to": "+1234567890",
  "lang": "en", 
  "year": 2040
}
```
**Result**: Agent speaks like someone from the AI Renaissance with expressions about neural networks and human-AI collaboration.

## Authentication and Example cURL

All API endpoints require a JWT. Obtain and use a token with these examples:

### Generate JWT Secret (for local .env)
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Get Token
```bash
TOKEN=$(curl -s -X POST https://your-api.com/auth/login | jq -r '.token')
```

### Check Rate Limit Status (optional)
```bash
curl -X GET https://your-api.com/rate-limit/status \
  -H "Authorization: Bearer $TOKEN"
```

### Make an Authenticated Call
```bash
curl -X POST https://your-api.com/outbound-call \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"to":"+1234567890","lang":"en","year":1350}'
```

## Testing

### Unit Tests
Run the comprehensive test suite:
```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test modules
poetry run pytest tests/test_rate_limiting.py -v
poetry run pytest tests/test_era_config.py -v
poetry run pytest tests/test_agent_manager.py -v
poetry run pytest tests/test_voice_manager.py -v
```

### Integration Testing
Make test calls with different years and check logs for:
```
Selected random agent: Time Traveler - Scholar
Using agent ID: abc12345... (Time Traveler - Scholar)
Selected voice: Spanish Voice 1 (ID: def67890...) - female young adult
Era: High Middle Ages (1350) - feudal order, chivalry, scholasticism
Expressions: "By my troth!", "The cathedral spires reach toward heaven..."
```

### Test Coverage
The project includes 49 unit tests covering:
- ✅ Rate limiting logic and dependencies
- ✅ Era configuration and mapping
- ✅ Agent and voice management
- ✅ Authentication and JWT handling
- ✅ Error handling and edge cases

## Quick Setup Checklist

- Create agents in ElevenLabs dashboard
- Add agent IDs to `.env` file
- Update `agents.json` with agent names
- Update `voices.json` with voice pools
- Configure system prompts in ElevenLabs dashboard
- Test with multiple calls to verify randomization
- Test different years to verify era configuration
- Test both English and Spanish to verify language support
```
