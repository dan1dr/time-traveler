# Time Traveler — Web (Next.js)

A clean, modern UI to initiate live calls with a time traveler agent. Users choose their phone number (with country code), language (EN/ES), and a year (0–5000+), then receive a real-time call via Twilio + ElevenLabs.

## Local Development

1) Install deps
```bash
cd apps/web
pnpm i # or: npm i / yarn
```

2) Configure backend URL (dev)
```bash
# Create .env.local
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

3) Run dev server
```bash
pnpm dev # or: npm run dev / yarn dev
# open http://localhost:3000
```

Ensure the backend is running and publicly reachable if Twilio requires it (e.g., via ngrok):
```bash
# in another terminal
cd apps/server
poetry run uvicorn main:app --reload --port 8000
ngrok http 8000
# set NEXT_PUBLIC_BACKEND_URL to the ngrok https URL if testing full Twilio flow
```

Note: If you run frontend on http://localhost:3000 and backend on http://localhost:8000, ensure CORS is enabled on the backend during development.

## Production Build
```bash
pnpm build
pnpm start
```

## Deployment

For complete deployment instructions including both frontend (Vercel) and backend (Railway/Render), see the comprehensive deployment guide:

📖 **[Complete Deployment Guide](../infra/deployment/README.md)**

### Quick Vercel Deployment

- **Project Root**: `apps/web`
- **Framework**: Next.js (auto-detected)
- **Build Command**: `pnpm build`
- **Install Command**: `pnpm i`
- **Environment Variables**:
  - `NEXT_PUBLIC_BACKEND_URL` — your public backend URL (https)

### Prerequisites

- Backend deployed and accessible (see deployment guide)
- Vercel and Railway account
- Environment variables configured

## UI Overview

- Country + phone input with validation
- Year slider showing era label and description
- Language toggle EN/ES
- Call button with loading state and inline feedback

## Notes

- This UI calls `POST /outbound-call` on the backend with `{ to, lang, year }`.
- Twilio Media Streams requires the backend to be publicly accessible during calls.
