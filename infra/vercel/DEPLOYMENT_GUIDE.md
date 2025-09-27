# Time Traveler - Vercel Deployment Guide

A comprehensive guide to deploy the Time Traveler project using Vercel for frontend and an external service for the Python backend.

## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP/WebSocket    ┌──────────────────┐
│   Vercel        │ ──────────────────── │ Railway/Render   │
│   (Frontend)    │                      │ (Backend)        │
│                 │                      │                  │
│ • Next.js App   │                      │ • FastAPI        │
│ • Static Assets │                      │ • WebSocket      │
│ • CDN           │                      │ • Python Deps    │
└─────────────────┘                      └──────────────────┘
```

## 📋 Prerequisites

- [x] GitHub repository with your Time Traveler code
- [x] Vercel account (free tier works)
- [x] Railway/Render account for backend
- [x] ElevenLabs API key
- [x] Twilio account with phone number

## 🚀 Part 1: Backend Deployment (Railway)

### Step 1: Prepare Backend for Deployment

Create the following files in `apps/server/`:

#### 1.1 Generate `requirements.txt`

```bash
cd apps/server
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
```

The requirements.txt will include the shared_py package automatically. Or manually create `apps/server/requirements.txt`:
```txt
fastapi==0.116.2
uvicorn[standard]==0.35.0
elevenlabs==2.15.0
twilio==9.8.0
python-dotenv==1.1.1
python-multipart==0.0.20
starlette==0.48.0
# Note: shared_py package will be installed via setup.py during deployment
```

#### 1.2 Create `Procfile`

Create `apps/server/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 1.3 Create `runtime.txt`

Create `apps/server/runtime.txt`:
```
python-3.11
```

### Step 2: Deploy to Railway

1. **Sign up**: Go to [railway.app](https://railway.app) and sign in with GitHub
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your `time-traveler` repository
4. **Configure Build**:
   - **Root Directory**: `apps/server`
   - **Build Command**: `pip install ../../packages/shared_py && pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Environment Variables**: Add these in Railway dashboard:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_key
   ELEVENLABS_AGENT_ID=your_agent_id
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_number
   DEBUG_LOGS=true
   ```

6. **Deploy**: Railway will automatically deploy
7. **Get URL**: Note your Railway app URL (e.g., `https://your-app.railway.app`)

### Step 3: Test Backend Deployment

```bash
# Test basic endpoint
curl https://your-app.railway.app/

# Test outbound call (replace with your Railway URL and phone)
curl -X POST https://your-app.railway.app/outbound-call \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "lang": "en", 
    "year": 1350
  }'
```

## 🌐 Part 2: Frontend Deployment (Vercel)

### Step 1: Connect Repository to Vercel

1. **Sign up**: Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. **Import Project**: Click "New Project" → Import your `time-traveler` repository
3. **Configure Build Settings**:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `apps/web`
   - **Build Command**: `npm run build`
   - **Output Directory**: Leave empty (auto-detected)
   - **Install Command**: `npm install`

### Step 2: Environment Variables

In Vercel dashboard, add environment variables:

#### For Development:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

#### For Preview:
```
NEXT_PUBLIC_BACKEND_URL=https://your-app.railway.app
```

#### For Production:
```
NEXT_PUBLIC_BACKEND_URL=https://your-app.railway.app
```

### Step 3: Configure Branch Strategy

1. **Production Branch**: Set `main` as production branch
2. **Preview Deployments**: Enable for all other branches
3. **Auto-Deploy**: Enable for easier iteration

## 🔄 Part 3: Development Workflow

### Branch Strategy

```
main (Production)     ──→ https://time-traveler.vercel.app
  ↑
dev (Preview)         ──→ https://time-traveler-git-dev-yourname.vercel.app
  ↑
feature/* (Preview)   ──→ https://time-traveler-git-feature-yourname.vercel.app
```

### Development Cycle

1. **Work on Feature Branch**:
   ```bash
   git checkout -b feature/new-era-support
   # Make changes to frontend/backend
   git push origin feature/new-era-support
   ```

2. **Preview Deployment**:
   - Vercel auto-creates preview URL
   - Test against your Railway backend
   - Share preview URL for feedback

3. **Promote to Production**:
   ```bash
   # Option 1: Merge to main
   git checkout main
   git merge feature/new-era-support
   git push origin main
   
   # Option 2: Promote directly in Vercel dashboard
   ```

### Testing Checklist

Before promoting to production:

- [ ] Preview deployment loads correctly
- [ ] Phone number input works
- [ ] Era selection functional
- [ ] Backend API calls succeed
- [ ] WebSocket connection establishes
- [ ] Test call completes successfully
- [ ] No console errors
- [ ] Mobile responsive

## 🛠️ Part 4: Configuration Files

### Vercel Configuration (Optional)

Create `apps/web/vercel.json` for advanced configuration:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_BACKEND_URL": {
      "development": "http://localhost:8000",
      "preview": "https://your-app.railway.app",
      "production": "https://your-app.railway.app"
    }
  }
}
```

### Environment File Templates

#### Backend `.env` template:
```bash
# Copy to apps/server/.env (DO NOT COMMIT)
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_AGENT_ID=agent_...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...
DEBUG_LOGS=true
```

#### Frontend `.env.local` template:
```bash
# Copy to apps/web/.env.local (DO NOT COMMIT)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 💰 Cost Estimation

### Vercel (Frontend)
- **Free Tier**: 100GB bandwidth, unlimited personal projects
- **Pro**: $20/month (for team features, more bandwidth)

### Railway (Backend)
- **Free Tier**: $5 credit monthly (500 hours)
- **Hobby**: $5/month for 500 hours
- **Pro**: $20/month for unlimited usage

### Total Monthly Cost (Hobby Level)
- **Development**: Free (local backend + Vercel free)
- **Production**: $5-10/month (Railway + Vercel free)

## 🚨 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Railway logs
railway logs

# Common fixes:
# 1. Verify Procfile syntax
# 2. Check Python version in runtime.txt
# 3. Ensure all dependencies in requirements.txt
```

#### Frontend Can't Reach Backend
```bash
# Check environment variables
# Verify CORS settings in FastAPI
# Test backend URL directly
curl https://your-app.railway.app/
```

#### WebSocket Connection Fails
```bash
# Check Railway supports WebSocket (it does)
# Verify Twilio webhook URL points to Railway
# Test WebSocket endpoint directly
```

### Environment Variable Issues

1. **Vercel**: Environment variables are scoped by environment (Development/Preview/Production)
2. **Railway**: Global environment variables for the service
3. **Rebuild**: Changes require redeployment on both platforms

## 🔒 Security Considerations

### Environment Variables
- Never commit `.env` files
- Use different API keys for staging/production if possible
- Rotate secrets regularly

### CORS Configuration
Ensure your FastAPI backend allows requests from your Vercel domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
        "https://*.vercel.app"  # For preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 Monitoring & Maintenance

### Vercel Monitoring
- View deployment status in dashboard
- Check function logs for errors
- Monitor bandwidth usage

### Railway Monitoring
- View application logs
- Monitor resource usage
- Set up uptime monitoring

### Regular Maintenance
- Update dependencies monthly
- Monitor API rate limits (ElevenLabs, Twilio)
- Review error logs weekly
- Test deployment pipeline monthly

---

## 🎯 Quick Start Checklist

- [ ] Backend: Create `requirements.txt`, `Procfile`, `runtime.txt`
- [ ] Backend: Deploy to Railway with environment variables
- [ ] Backend: Test API endpoints work
- [ ] Frontend: Connect repository to Vercel
- [ ] Frontend: Configure build settings for `apps/web`
- [ ] Frontend: Set environment variables per environment
- [ ] Frontend: Test preview deployment
- [ ] Integration: Test full call flow on preview
- [ ] Production: Promote to main branch
- [ ] Monitoring: Set up error tracking and uptime monitoring

For questions or issues, check the troubleshooting section or create an issue in the repository.
