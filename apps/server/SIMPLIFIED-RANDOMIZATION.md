# Randomization System - Technical Implementation

> **Note**: For setup instructions, see the main [README.md](README.md). This document covers the technical implementation details of the randomization system.

## System Overview

The randomization system uses pure randomization with era context coming from dynamic variables. This approach maximizes variety while maintaining character consistency.

## Technical Implementation

### Voice Selection
```python
# Language-based randomization with metadata
selected_voice = voice_manager.get_random_voice_for_language("es")
# Returns: {"id": "UOIqAnmS11Reiei1Ytkc", "name": "Spanish Voice 1", "gender": "female", "age_range": "young adult"}
```

### Agent Selection  
```python
# Simple random agent selection
selected_agent = agent_manager.get_random_agent()
# Returns: {"name": "Time Traveler - Scholar", "env_var": "ELEVENLABS_AGENT_ID_1"}
```

### Era Context
```python
# Rich era context from era_config.py
session_vars = get_era_session_variables(1350, "es")
# Returns: era_name, expressions, voice_settings, context, etc.
```

## Call Flow Example

**Request**: `{to: "+34...", lang: "es", year: 1350}`

**Randomization**:
- Voice: Random Spanish voice (e.g., `UOIqAnmS11Reiei1Ytkc`, female, young adult)
- Agent: Random agent (e.g., `Time Traveler - Mystic`)
- First Message: Random era-appropriate greeting

**Era Context** (from era_config.py):
- Era: Medieval (1350)
- Expressions: `"¡Por mi fe!"`, `"En estos tiempos oscuros..."`
- Voice settings: speed=1.0, stability=0.75
- Context: "medieval chivalry, feudalism, religious devotion"

**Character Consistency**:
- Voice metadata: female, young adult
- Dynamic variables include `voice_gender` and `voice_age_range`
- LLM creates character matching voice characteristics

**Result**: 
- Female young adult Spanish voice with medieval characteristics
- Time Traveler - Mystic personality with consistent character
- Era-specific first message and context injected via dynamic variables
- LLM adapts to be a young female mystical medieval Spanish time traveler

## System Design

- **Voice randomization**: Who speaks (random, with gender/age metadata)
- **Agent randomization**: Personality flavor (random)
- **Era context**: How/what they say (from era_config.py)
- **Voice characteristics**: Speaking style (from era_config.py)
- **First messages**: Era-specific greetings (random selection)
- **Character consistency**: Voice metadata ensures character alignment

**Result**: Maximum variety with authentic era context, character consistency, and enhanced immersion!
