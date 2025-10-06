# Twilio Voice Setup

A practical guide to configure Twilio for Time Traveler calls (outbound-first), both for local testing (ngrok) and production (Railway).

## Prerequisites

- Twilio account (trial or paid)
- ElevenLabs API key configured in backend
- Railway backend deployed (production) or local server with ngrok (testing)

Backend base URLs (examples):
- Testing (ngrok): `https://<your-ngrok-subdomain>.ngrok.io`
- Production (Railway): `https://<your-railway-url>.railway.app`

Use E.164 format for phone numbers (e.g., `+14155551234`).
 
## 1) Buy a Twilio Number (Voice-enabled)

1. Twilio Console → Phone Numbers → Buy a Number
2. Filter by Voice capability → Purchase
3. Recommended: US number for simplest routing during testing

## 2) Trial Account Limitations (Important)

If using a Twilio Free Trial:
- Your Twilio number is free (usually a US number)
- You can only call or receive calls with numbers you have verified
- Verify numbers in Console → Phone Numbers → Verified Caller IDs
- Twilio plays a trial message at call start (cannot be removed on trial)
- Some international calling is blocked on trial accounts

## 3) Outbound Calling Permissions (Geo)

Allow the countries you will call to:
1. Console → Voice → Settings → Geo permissions (or Dialing Permissions)
2. Enable outbound calling for the destination countries (e.g., United States, your target regions)
3. Save changes

Note: On trial, even with permissions enabled, you can only call verified numbers.

## 4) Webhook To Configure (only one)

Set your Twilio number's Voice webhook to POST the following URL. This is the only URL you need to configure. Our backend handles the rest of the flow with Twilio.

- Webhook (A call comes in): `POST {BASE_URL}/outbound-call`

Where `{BASE_URL}` is your public backend URL (ngrok for testing or Railway for production).

### Testing (ngrok)

Quickest path (no frontend required):
1. Run backend locally:
   ```bash
   cd apps/server
   uvicorn main:app --reload --port 8000
   ```
2. Expose it:
   ```bash
   ngrok http 8000
   ```
3. Twilio Console → Your Number → Voice → A Call Comes In:
   - Webhook: `https://<your-ngrok-subdomain>.ngrok.io/outbound-call`
   - Method: `HTTP POST`
4. Trigger a call with cURL (replace phone):
   ```bash
   curl -X POST https://<your-ngrok-subdomain>.ngrok.io/outbound-call \
     -H "Content-Type: application/json" \
     -d '{
       "to": "+1XXXXXXXXXX",
       "lang": "en",
       "year": 1350
     }'
   ```
5. Answer the phone. Watch backend logs for dynamic vars and voice/agent selection.

Optional (UI flow): set `NEXT_PUBLIC_BACKEND_URL` to your ngrok URL and start the web app to initiate calls from the UI.

### Production (Railway)

- Frontend → set `NEXT_PUBLIC_BACKEND_URL=https://<your-railway-url>.railway.app`
- Phone Number → Voice → A Call Comes In:
  - Webhook: `https://<your-railway-url>.railway.app/outbound-call`
  - Method: `HTTP POST`

## 5) Environment Variables (Backend)

Configure in Railway (or local `.env`):
```
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
ELEVENLABS_API_KEY=sk_...

# Agents (at least one required)
ELEVENLABS_AGENT_ID_1=agent_...
# Optional additional agents
ELEVENLABS_AGENT_ID_2=agent_...
ELEVENLABS_AGENT_ID_3=agent_...

# CORS (include your frontend)
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
DEBUG_LOGS=true
```

## 6) End-to-End Test (Local, cURL-first)

1. Start backend locally (`uvicorn ... --port 8000`)
2. Run `ngrok http 8000`
3. Set your number's Voice webhook → POST `https://<ngrok>.ngrok.io/outbound-call`
4. Call via cURL (replace phone):
   ```bash
   curl -X POST https://<ngrok>.ngrok.io/outbound-call \
     -H "Content-Type: application/json" \
     -d '{"to":"+1XXXXXXXXXX","lang":"en","year":1550}'
   ```
5. Answer the call; speak normally (barge-in supported). Check logs for era/dynamic vars.

If anything fails, check Twilio call logs and backend logs. Ensure your backend URL is publicly reachable (ngrok/Railway) and that destination country permissions are enabled.

