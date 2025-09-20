# Era Configuration System

This document explains how the Time Traveler agent adapts its personality, expressions, and voice to different historical eras based on the `year` and `lang` parameters.

## How It Works

### 1. API Call with Era Parameters

```bash
curl -X POST https://your-domain.com/outbound-call \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "lang": "en",
    "year": 1350
  }'
```

### 2. Era Mapping

The system automatically maps the year to a historical era:

- **Ancient Times** (0-500 AD): "By the gods!", philosophical wisdom
- **Medieval Era** (500-1500): "By my troth!", chivalry and feudalism  
- **Renaissance** (1400-1600): "What a marvel!", artistic discovery
- **Baroque Era** (1600-1750): "Most gracious indeed!", court refinement
- **Industrial Revolution** (1750-1900): "What progress!", steam and steel
- **Early 20th Century** (1900-1950): "What a time to be alive!", modern innovations
- **Mid-Late 20th Century** (1950-2000): "Far out, man!", space age and cultural revolution
- **21st Century** (2000+): "Amazing how connected we are...", digital age

### 3. Language Support

Each era includes expressions in both English (`en`) and Spanish (`es`):

```python
# Example for Medieval Era (1350)
"en": ["By my troth!", "In these dark times...", "The lord of the manor has decreed..."]
"es": ["¡Por mi fe!", "En estos tiempos oscuros...", "El señor del feudo ha decretado..."]
```

### 4. Agent Configuration

The system configures the ElevenLabs agent with:

- **Era-specific expressions**: 2-3 authentic phrases from the time period
- **Context hints**: Background about the era's culture and characteristics  
- **Voice settings**: Optimized stability, similarity, and style for each era
- **Language**: Responses in the specified language

## Environment Variables (Optional)

For even more customization, you can create era-specific agent IDs:

```bash
# Default agent (required)
ELEVENLABS_AGENT_ID=your_main_agent_id

# Era-specific agents (optional)
ELEVENLABS_AGENT_ID_MEDIEVAL=medieval_agent_id
ELEVENLABS_AGENT_ID_RENAISSANCE=renaissance_agent_id
ELEVENLABS_AGENT_ID_INDUSTRIAL=industrial_agent_id
# ... etc
```

If era-specific agent IDs are provided, the system will use them. Otherwise, it falls back to the main agent with era-appropriate context.

## Example Usage

### Medieval Knight (1350, English)
```json
{
  "to": "+1234567890",
  "lang": "en", 
  "year": 1350
}
```
**Agent behavior**: "By my troth! In these dark times, what brings thee to seek counsel from one who has witnessed the rise and fall of kingdoms?"

### Renaissance Artist (1550, Spanish)  
```json
{
  "to": "+1234567890",
  "lang": "es",
  "year": 1550  
}
```
**Agent behavior**: "¡Qué maravilla de la naturaleza! En el espíritu del descubrimiento, he visto nacer obras que rivalizan con los dioses mismos."

### 1960s Hippie (1968, English)
```json
{
  "to": "+1234567890", 
  "lang": "en",
  "year": 1968
}
```
**Agent behavior**: "Far out, man! The space age is upon us and it's like, totally changing how we see the universe, you know?"

## Technical Implementation

The era configuration system works through:

1. **`era_config.py`**: Maps years to historical eras with expressions and settings
2. **API Parameters**: `{to, lang, year}` passed through the entire call flow
3. **Agent Initialization**: Era context applied when starting ElevenLabs conversation
4. **Dynamic Selection**: Automatically chooses appropriate era based on year input

## Customization

To add new eras or modify existing ones, edit `era_config.py`:

```python
# Add new era configuration
(start_year, end_year): EraConfig(
    era_name="your_era",
    description="Era description", 
    expressions={
        "en": ["English expressions..."],
        "es": ["Spanish expressions..."]
    },
    voice_settings={"stability": 0.7, "similarity_boost": 0.8, "style": 0.5},
    context_hint="Era cultural context",
    time_period="Display Name"
)
```

The agent will automatically use this configuration for years within the specified range.
