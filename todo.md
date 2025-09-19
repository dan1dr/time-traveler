# Time-Traveler Backend & Packages TODO

Based on the current implementation analysis and the planned architecture in `repo-structure.md`, here are the remaining features to implement for the backend and packages:

## Backend API Restructuring

### 🔄 API Endpoints (High Priority)
- [ ] **Update `/outbound-call` endpoint**: Change from form data to JSON body accepting `{to, lang, year, voice}`
- [x] **Keep `/outbound-call-twiml` endpoint**: Functionality already correct ✅
- [ ] **Fix WebSocket route**: Add missing `@app.websocket('/outbound-media-stream')` decorator

### 📁 Backend Architecture Modules
- [ ] **Create `app/settings.py`**: Implement pydantic-settings based environment loader
- [ ] **Create `app/era_hints.py`**: Module to map year → era "vibe" strings (ES/EN)
- [ ] **Create `app/eleven_agent.py`**: ElevenLabs Conversation bootstrap with session variables
- [ ] **Refactor to `app/twilio_bridge.py`**: Enhanced audio bridge with better μ-law ↔ PCM16 conversion
- [ ] **Restructure `main.py`**: Organize routes according to TRD architecture

## Shared Content System

### 📋 Content Structure
- [ ] **Create `packages/shared-content/eras/`**:
  - `eras.es.json` - Spanish era motifs/expressions
  - `eras.en.json` - English era motifs/expressions
- [ ] **Create `packages/shared-content/voices/`**:
  - `voices.es.json` - Spanish curated voice IDs + labels  
  - `voices.en.json` - English curated voice IDs + labels

### 🐍 Python Package Integration
- [ ] **Create `packages/shared-py/`**: Python helpers to consume shared-content JSON
- [ ] **Backend integration**: Connect shared-content to backend for era hints and voice selection

## Agent Enhancement

### 🤖 ElevenLabs Agent Configuration
- [ ] **System prompt implementation**: Era expressions, sensory motifs with session variables
- [ ] **Session variable handling**: `{year, language, voice_id, era_hint}` per call
- [ ] **Short response optimization**: Configure agent for ≤3 sentences, barge-in enabled

## Audio & Communication

### 🔊 Audio Processing
- [ ] **Enhanced audio conversion**: Improve μ-law 8k → PCM16 16k conversion quality
- [ ] **Barge-in optimization**: Better interrupt handling for user speech detection
- [ ] **Error handling**: Robust audio stream error recovery

## Configuration & Validation

### ⚙️ Environment & Settings
- [ ] **Comprehensive env validation**: Validate all required environment variables
- [ ] **Error handling**: Graceful degradation and meaningful error messages
- [ ] **Debug logging**: Structured logging with configurable levels

---

## Current Status
✅ **Completed**: Basic outbound call functionality with Twilio and ElevenLabs integration  
🔧 **In Progress**: None  
📋 **Next Priority**: API endpoint restructuring and shared content system

## Notes
- Current implementation uses form-based `/outbound-call` - needs migration to JSON `/api/call`
- Missing all shared content structure (eras, voices)
- Agent lacks era-specific personality configuration
- Audio processing needs enhancement for production quality
