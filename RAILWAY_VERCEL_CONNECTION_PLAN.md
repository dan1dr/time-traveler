# 🚀 Railway + Vercel Connection Plan

## 📋 Overview

This plan connects your Railway backend with your Vercel frontend, configures CORS properly, and sets up the complete deployment pipeline.

## 🎯 Current Status

- ✅ **Frontend**: Deployed on Vercel (working)
- ✅ **Backend**: Deployed on Railway (working)
- ✅ **Connection**: CORS configured and working
- ✅ **Environment Variables**: Configured for production
- ✅ **Full Call Flow**: End-to-end working

---

## 🔧 Step 1: Backend CORS Configuration

### 1.1 Add CORS Middleware to FastAPI

**File**: `apps/server/main.py`

**Action**: Add after line 40 (after `app = FastAPI(...)`)

```python
from fastapi.middleware.cors import CORSMiddleware

# Environment-based CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Debug logging for CORS
if DEBUG_LOGS:
    print(f"🔗 CORS configured for origins: {ALLOWED_ORIGINS}")
```

### 1.2 Add CORS to Requirements

**File**: `apps/server/requirements.txt`

**Action**: Verify `fastapi[all]` is included or add manually:

```txt
fastapi[all]==0.116.2
```

---

## 🌐 Step 2: Railway Environment Variables

### 2.1 Production Environment Variables

**Platform**: Railway Dashboard → Environment Variables

**Add these variables**:

```bash
# CORS Configuration
ALLOWED_ORIGINS=https://your-production-domain.vercel.app,http://localhost:3000

# Existing variables (verify these exist)
ELEVENLABS_API_KEY=sk_your_key_here
ELEVENLABS_AGENT_ID=agent_your_id_here
TWILIO_ACCOUNT_SID=AC_your_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
DEBUG_LOGS=true

# Safety flag for production
ENVIRONMENT=production
```


---

## 🎨 Step 3: Vercel Environment Variables

### 3.1 Production Environment

**Platform**: Vercel Dashboard → Settings → Environment Variables → Production

```bash
NEXT_PUBLIC_BACKEND_URL=https://your-railway-app.railway.app
```

### 3.2 Preview Environment

**Platform**: Vercel Dashboard → Settings → Environment Variables → Preview

```bash
NEXT_PUBLIC_BACKEND_URL=https://your-railway-app.railway.app
```

### 3.3 Development Environment

**Platform**: Vercel Dashboard → Settings → Environment Variables → Development

```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 🔧 Step 4: Twilio Webhook Configuration

### 4.1 Update Twilio Webhook URL

**Platform**: Twilio Dashboard → Phone Numbers → Manage → Active Numbers

**Action**: Update webhook URL for outbound calls

```bash
# Current (ngrok for local development)
https://cdcbcd5edc3c.ngrok-free.app/twilio/inbound_call

# New (Railway production)
https://time-traveler-production.up.railway.app/outbound-call-twiml
```

**Method**: HTTP GET

---

## 🔄 Step 5: Deployment Sequence

### 5.1 Backend Deployment

1. **Update Code**: Add CORS middleware to `main.py`
2. **Commit & Push**: Push changes to trigger Railway deployment
3. **Set Environment Variables**: Configure Railway environment variables
4. **Test Backend**: Verify Railway app is accessible

### 5.2 Frontend Configuration

1. **Set Environment Variables**: Configure Vercel environment variables
2. **Test Connection**: Verify frontend can reach backend
3. **Deploy**: Push any needed changes to trigger Vercel deployment

### 5.3 Integration Testing

1. **CORS Test**: Check browser developer tools for CORS errors
2. **API Test**: Verify `/outbound-call` endpoint works
3. **End-to-End Test**: Complete call flow test

---

## 🧪 Step 6: Testing Checklist

### 6.1 CORS Verification

- [ ] **Browser DevTools**: No CORS errors in console
- [ ] **Network Tab**: Successful OPTIONS and POST requests
- [ ] **Response Headers**: `Access-Control-Allow-Origin` present

### 6.2 Environment Testing

- [ ] **Production**: Real calls work from production domain
- [ ] **Preview**: Preview deployments work with same backend
- [ ] **Development**: Local development works

### 6.3 API Testing

```bash
# Test CORS with curl
curl -X OPTIONS https://your-railway-app.railway.app/outbound-call \
  -H "Origin: https://your-production-domain.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Test actual endpoint
curl -X POST https://your-railway-app.railway.app/outbound-call \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-production-domain.vercel.app" \
  -d '{"to": "+15551234567", "lang": "en", "year": 1950}' \
  -v
```

---

## 🚨 Step 7: Troubleshooting Guide

### 7.1 Common CORS Issues

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`
**Solution**: Verify CORS middleware is added and Railway environment variables are set

**Problem**: `CORS policy: The request client is not a secure context`
**Solution**: Ensure both frontend and backend use HTTPS in production

### 7.2 Environment Variable Issues

**Problem**: Backend returns 500 errors
**Solution**: Check Railway logs for missing environment variables

**Problem**: Frontend shows "Could not reach server"
**Solution**: Verify `NEXT_PUBLIC_BACKEND_URL` is set correctly in Vercel

### 7.3 Twilio Webhook Issues

**Problem**: Calls fail with 500 errors
**Solution**: Verify Twilio webhook URL points to correct Railway endpoint

---

## 📚 Step 8: Documentation Updates

### 8.1 Update README.md

**File**: `apps/server/README.md`

**Add section**:
```markdown
## Environment Variables

### Required for Production
- `ALLOWED_ORIGINS`: Comma-separated list of allowed frontend origins
- `ENVIRONMENT`: Set to "production" for production deployment
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number

### Optional
- `USE_TEST_MODE`: Set to "true" to enable test mode
- `DEBUG_LOGS`: Set to "true" to enable debug logging
```

### 8.2 Update Deployment Guide

**File**: `infra/deployment/README.md`

**Update with**:
- CORS configuration steps
- Environment variable setup for both platforms
- Twilio webhook configuration

---

## ✅ Success Criteria

- [ ] **CORS**: No CORS errors in browser console
- [ ] **API Connection**: Frontend successfully calls backend
- [ ] **Twilio Integration**: Webhook properly configured
- [ ] **Environment Variables**: All required variables set
- [ ] **Monitoring**: Debug logs show successful connections
- [ ] **End-to-End**: Complete call flow works in production

---

## 🔗 Final URLs to Configure

**Replace these placeholders with actual values**:

- `your-railway-app.railway.app` → `time-traveler-production.up.railway.app`
- `your-production-domain.vercel.app` → Your actual Vercel production URL
