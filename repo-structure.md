# Time-Traveler Hotline — MVP Repo Guide (PRD + TRD)

A compact, single-page reference for structure, flow, and how to run.

---

## Overview

This project delivers an **outbound voice experience**: a visitor submits a form (phone, language, year) and immediately receives a call. On pickup, a **live ElevenLabs Agent** converses naturally with era-flavored style.  

- **Web (Next.js / Vercel)** – minimal form to trigger the call.  
- **Server (FastAPI)** – initiates **Twilio** outbound call and bridges **Twilio Media Streams** ↔ **ElevenLabs Agent** for real-time conversation.  
- **Shared content** – era “vibe” packs + curated voice IDs, consumed by both apps.

---

## High-Level Call Flow

```mermaid
sequenceDiagram
  autonumber
  participant U as User (Web)
  participant V as Vercel (UI)
  participant B as FastAPI (Server)
  participant T as Twilio Voice
  participant W as Twilio WS Stream
  participant E as ElevenLabs Agent

  U->>V: Submit {phone, lang, year, voice?}
  V->>B: POST /api/call
  B->>T: Calls.create(from, to, url=/twilio/voice?year&lang&voice)
  T-->>B: 201 (Call SID)
  T->>B: GET/POST /twilio/voice (on answer)
  B-->>T: TwiML <Connect><Stream url="wss://.../media" params>
  T->>W: Open WSS (bidirectional)
  W->>B: event=start {streamSid, params}
  B->>E: Conversation.start_session({year, language, voice_id, era_hint})
  T->>B: event=media (μ-law 8k frames)
  B->>E: feed_input_audio(PCM16 16k)  (convert if needed)
  E-->>B: output(audio PCM16 16k)
  B-->>T: event=media (base64 audio)
  U-->>T: Speaks / barge-in
  T->>B: more media frames
  B->>E: interrupt(); feed_input_audio(...)
  E-->>B: new response turns
  B-->>T: event=media (audio back)
  T-->>U: Plays agent replies
  U-->>T: Hangs up
  T->>B: event=stop / status
  B->>E: end_session(); wait_for_session_end()
````

---

## Repository Structure

```
time-traveler/
├─ apps/
│  ├─ web/                      # Next.js (Vercel) UI
│  └─ server/                   # FastAPI backend (Poetry)
├─ packages/
│  ├─ shared-content/           # JSON: eras & voices (single source of truth)
│  ├─ shared-py/                # Python adapter to load that JSON
│  └─ shared-ts/                # TypeScript adapter to load that JSON
├─ infra/
│  ├─ vercel/                   # Vercel config/notes (UI)
│  ├─ docker/                   # Dockerfiles/compose (optional)
│  └─ twilio/                   # Number setup, Media Streams notes
├─ scripts/                     # Dev helpers (no app logic)
├─ .env.example                 # Documentation of all env vars across apps
├─ README.md
├─ package.json                 # JS workspaces root (web + shared-ts)
└─ (per-app) pyproject.toml     # Poetry files inside Python subprojects
```

### Folder Purposes (concise)

* **apps/web/** – Public UI (form).

  * `src/app/page.tsx` — landing form.
  * *(Optional)* `src/app/api/call/route.ts` — proxy → backend `/api/call`.
  * `src/components/` — `YearSlider`, `PhoneInput`, `VoiceSelect`.
  * **Env:** `apps/web/.env.local` with only `NEXT_PUBLIC_*` vars.

* **apps/server/** – Backend (FastAPI).

  * `app/main.py` — routes: `POST /api/call`, `GET|POST /twilio/voice`, `WS /media`.
  * `app/twilio_bridge.py` — μ-law 8k ↔ PCM16 16k bridge + barge-in handling.
  * `app/eleven_agent.py` — ElevenLabs Conversation bootstrap; session vars (year/lang/voice, era hint).
  * `app/era_hints.py` — map year → era “vibe” strings (ES/EN).
  * `app/settings.py` — env loader (pydantic-settings).
  * **Env:** `apps/server/.env` (secrets, git-ignored).

* **packages/shared-content/** — JSON only (source of truth).

  * `eras/eras.es.json`, `eras/eras.en.json` — motifs/expressions.
  * `voices/voices.es.json`, `voices/voices.en.json` — curated voice IDs + labels.

* **packages/shared-py/** — Python helpers to consume JSON from server.

* **packages/shared-ts/** — TS helpers to consume JSON from web.

* **infra/** — Deploy notes/configs (Vercel, Docker, Twilio).

* **scripts/** — Convenience scripts (start dev server + ngrok, sample curl).

---

## PRD (MVP)

* **Goal:** After form submit, user gets a **live** call from a “Time Traveler” (ES/EN) with era-flavored cadence.
* **In scope:** UI form → backend outbound call; Twilio Media Streams; ElevenLabs Agent (barge-in ON, short turns).

---

## TRD (MVP)

**Frontend (Next.js / Vercel)**

* Posts to backend `POST /api/call` with body `{ to, lang, year}`.

**Backend (FastAPI)**

* `POST /api/call` → Twilio `Calls.create(from, to, url=/twilio/voice?year&lang&voice)`
* `GET|POST /twilio/voice` → TwiML `<Connect><Stream wss://.../media>` (pass year/lang/voice as `<Parameter>`).
* `WS /media` → Handle Twilio events:

  * `start` — open ElevenLabs Conversation with session vars `{year, language, voice_id, era_hint}`.
  * `media` — convert Twilio μ-law 8k → PCM16 16k (if needed), feed agent; send agent audio back as base64 `media`.
  * `stop` — end session, cleanup.

**Audio & Barge-in**

* Convert μ-law 8k → PCM16 16k before feeding the agent; agent output is PCM16 16k; send back as Twilio `media` events.
* On user speech, call `interrupt()` to clear outgoing audio quickly.

**Agent (ElevenLabs)**

* One Agent; barge-in enabled; short responses (≤3 sentences).
* System prompt (concept): modern ES/EN, **2–4 era expressions**, sensory motifs; avoid archaic orthography; ask one curiosity question; avoid specific present-day claims (celebrities/politics/medical/finance).
* Session vars per call: `{year, language, voice_id, era_hint}`.

**Security**

* HTTPS/WSS; verify Twilio signatures (post-MVP); git-ignore env files; basic per-phone rate limit if needed.

**Deployment**

* Web → Vercel.
* Server → small always-on host (Fly/Render/EC2) with public HTTPS (ngrok for dev).
* Twilio number (voice capable) with Media Streams enabled.

---

## Environment Variables

**Backend (`apps/server/.env`)**

```
ELEVENLABS_API_KEY=
ELEVENLABS_AGENT_ID=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=+34...
PUBLIC_BASE_URL=https://your-public-server
DEBUG_LOGS=true
```

**Frontend (`apps/web/.env.local`)**

```
NEXT_PUBLIC_BACKEND_URL=https://your-public-server
# (No secrets here)
```

**Root (`.env.example`)** — documents all vars; do **not** commit real secrets.

---

## Quickstart (Dev)

```bash
# Backend
cd apps/server
poetry install
poetry run uvicorn app.main:app --reload --port 8000
ngrok http 8000   # copy HTTPS URL into apps/server/.env as PUBLIC_BASE_URL

# Test a call (no UI yet)
curl -X POST "$PUBLIC_BASE_URL/api/call" \
  -H "Content-Type: application/json" \
  -d '{"to":"+34XXXXXXXXX","year":1580,"lang":"es"}'

# Frontend (optional later)
cd ../../apps/web
pnpm i
pnpm dev
# set NEXT_PUBLIC_BACKEND_URL in apps/web/.env.local to your server URL
```

---

## Conventions

* **Single source of truth** for eras/voices in `packages/shared-content/`.
* **Frontend never stores secrets** (only `NEXT_PUBLIC_*` vars).
* Keep agent turns short to reduce latency; verify **barge-in** behavior.
* Supabase/DB not required for MVP; add later for rate-limits or content editing.

