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

## Deploying to Vercel

- Recommended: Connect the repo to Vercel and set the project root to `apps/web`.
- Environment Variables:
  - `NEXT_PUBLIC_BACKEND_URL` — your public backend URL (https).
- Build & Output:
  - Framework: Next.js
  - Build Command: `pnpm build`
  - Install Command: `pnpm i`
  - Output: automatically handled by Next
- If using monorepo:
  - Set Project Settings → Root Directory: `apps/web`
  - Optionally enable Turborepo (not required here)

## UI Overview

- Country + phone input with validation
- Year slider (0–5000+) showing era label and description
- Language toggle EN/ES
- Call button with loading state and inline feedback

## Notes

- This UI calls `POST /outbound-call` on the backend with `{ to, lang, year }`.
- Twilio Media Streams requires the backend to be publicly accessible during calls.
