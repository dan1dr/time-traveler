# ElevenLabs Agent Setup Guide

This guide explains how to configure multiple ElevenLabs agents to work with the voice and agent randomization system.

## Agent Configuration

The system now supports multiple agent personalities that are randomly selected per call. Each agent should have a slightly different system prompt to create varied conversation experiences.

### Environment Variables Required

Configure these environment variables in your `.env` file:

```bash
# Base agent (required)
ELEVENLABS_AGENT_ID=agent_base_id_here

# Optional alternate agents for varied personas
ELEVENLABS_AGENT_ID_ALT_1=agent_scholar_id_here
ELEVENLABS_AGENT_ID_ALT_2=agent_adventurer_id_here  
ELEVENLABS_AGENT_ID_ALT_3=agent_mystic_id_here
ELEVENLABS_AGENT_ID_ALT_4=agent_artisan_id_here

# Voice pools per language (comma-separated)
ELEVENLABS_VOICES_ES=gD1IexrzCvsXPHUuT0s3,ntkgXc9uETkrSWUa2Gja,I0RpMYnjlWe6hUgHLXrb,E3MrNtjUaYrNQEr9YqXs
ELEVENLABS_VOICES_EN=aOZ9Pl8uWUTet0DS7PYP,VWQuOfcP7ILB48IXXGXE,G17SuINrv2H9FC6nvetn,iBo5PWT1qLiEyqhM7TrG
```

### System Prompt Template

Each agent should use this base system prompt with dynamic variables, but add personality-specific modifications:

```
You are a time traveler from the year {{era_year}} during the {{time_period}}.

HISTORICAL CONTEXT: {{era_context}}

LANGUAGE: Always respond in {{language_name}}.

PERSONALITY: Use these expressions naturally:
- "{{expression_1}}"
- "{{expression_2}}"  
- "{{expression_3}}"

[PERSONALITY-SPECIFIC SECTION - customize per agent]

Keep responses to 3 sentences or less. Be curious about the present day.
```

### Agent Personality Variations

All agents use the same base system prompt with dynamic variables, but can have subtle personality differences:

#### Time Traveler - Standard (Base Agent)
```
You are naturally curious and observant, asking thoughtful questions about modern life while sharing fascinating details from your era.
```

#### Time Traveler - Scholar (ALT_1)
```
You approach conversations with deep intellectual curiosity, analyzing the patterns of history and drawing connections between your time and the present. You're particularly interested in knowledge and learning.
```

#### Time Traveler - Adventurer (ALT_2)  
```
You're bold and energetic, filled with exciting tales from your era. You're drawn to stories of discovery and the thrill of experiencing different times.
```

#### Time Traveler - Mystic (ALT_3)
```
You speak with poetic wisdom about the cosmic nature of time and existence. You're contemplative, offering insights about the connections between all eras.
```

#### Time Traveler - Artisan (ALT_4)
```
You're passionate about the creative arts and craftsmanship of your era. You speak with appreciation for beauty and artistic expression across time.
```

**Note**: Agent selection is now **randomized** and **era-agnostic**. The era context comes through dynamic variables, not agent-specific knowledge.

## Agent Dashboard Configuration

### Required Settings

In the ElevenLabs Agent Dashboard for each agent:

1. **Enable Overrides**: Turn on all override options:
   - ✅ Voice ID
   - ✅ Voice Speed  
   - ✅ Voice Stability
   - ✅ Voice Similarity
   - ✅ Voice Style
   - ✅ System Prompt
   - ✅ Language

2. **System Prompt**: Use the template above with personality-specific modifications

3. **Default Voice**: Set a reasonable default voice for each language

4. **Conversation Settings**:
   - Enable barge-in
   - Set response length to short (≤3 sentences)
   - Enable dynamic variables

### Testing Agent Randomization

To test that multiple agents are working:

1. Make several test calls with the same parameters
2. Check the logs for different agent selections:
   ```
   🤖 Selected random agent: Time Traveler - Scholar
   🎯 Using agent ID: abc12345... (Time Traveler - Scholar)
   ```
3. Listen for different personality traits in conversations
4. Note that era context comes from dynamic variables, not agent-specific prompts

### Fallback Behavior

- If alternate agent IDs are not configured, the system falls back to the base `ELEVENLABS_AGENT_ID`
- If voice pools are empty, the system uses the agent's default voice
- All error conditions are logged for debugging

## Voice Pool Configuration  

The system randomly selects from curated voice pools defined in:
- `packages/shared-content/voices.json` (primary)
- Environment variables `ELEVENLABS_VOICES_ES` and `ELEVENLABS_VOICES_EN` (fallback)

Each voice in the JSON includes era preferences to improve voice-era matching while maintaining randomization.