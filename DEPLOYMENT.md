# 🚀 YogaFlow Deployment Guide

## **Deployment Strategy**

### **Frontend (React) → Vercel**
### **Backend (Flask) → Railway**
### **Database → Supabase (already set up)**

---

## **🔧 Step 1: Fix CORS Configuration**

Your CORS is now configured to handle multiple environments automatically.

### **Environment Variables for CORS:**
```env
# Development (multiple localhost ports)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Production (your deployed frontend URLs)
CORS_ORIGINS=https://yogaflow.vercel.app,https://yourdomain.com
```

---

## **🌐 Step 2: Deploy Frontend to Vercel**

### **2.1 Connect to Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Set root directory to: `frontend/yogafrontend`

### **2.2 Configure Build Settings:**
- **Framework Preset:** Create React App
- **Root Directory:** `frontend/yogafrontend`
- **Build Command:** `npm run build`
- **Output Directory:** `build`

### **2.3 Environment Variables:**
Add these in Vercel dashboard:
```env
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

---

## **⚡ Step 3: Deploy Backend to Railway**

### **3.1 Connect to Railway:**
1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Set root directory to: `backend`

### **3.2 Environment Variables:**
Add these in Railway dashboard:
```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-production-key-here

# CORS Configuration (replace with your Vercel URL)
CORS_ORIGINS=https://yogaflow.vercel.app

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
```

---

## **🔐 Step 4: Environment Variables Setup**

### **4.1 Generate Production Secrets:**
```bash
# Generate secure random keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### **4.2 Supabase Keys:**
1. Go to your Supabase project dashboard
2. Settings → API
3. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** → `SUPABASE_ANON_KEY`
   - **service_role** → `SUPABASE_SERVICE_ROLE_KEY`

### **4.3 OpenAI API Key:**
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Copy your API key → `OPENAI_API_KEY`

---

## **🔄 Step 5: Update Frontend API URL**

After deploying backend, update your frontend:

### **5.1 Update API Service:**
In `frontend/yogafrontend/src/services/api.ts`, the API_BASE_URL will automatically use:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

### **5.2 Set Environment Variable in Vercel:**
```env
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

---

## **✅ Step 6: Test Deployment**

### **6.1 Test Backend:**
```bash
curl https://your-backend-url.railway.app/api/flow/test
```

### **6.2 Test Frontend:**
1. Go to your Vercel URL
2. Try signing up/logging in
3. Generate a yoga flow

---

## **🚀 Alternative Deployment Options**

### **Backend Alternatives:**
- **Render:** [render.com](https://render.com) (free tier)
- **Heroku:** [heroku.com](https://heroku.com) (paid)
- **DigitalOcean App Platform:** [digitalocean.com](https://digitalocean.com)

### **Frontend Alternatives:**
- **Netlify:** [netlify.com](https://netlify.com) (free tier)
- **GitHub Pages:** For static sites
- **AWS Amplify:** [aws.amazon.com/amplify](https://aws.amazon.com/amplify)

---

## **🔧 Troubleshooting**

### **CORS Issues:**
- Make sure `CORS_ORIGINS` includes your exact frontend URL
- Check for trailing slashes
- Verify HTTPS vs HTTP

### **Environment Variables:**
- Double-check all keys are set correctly
- No spaces around the `=` sign
- Restart your deployment after changing env vars

### **Database Connection:**
- Verify Supabase URL and keys
- Check if your Supabase project is active
- Ensure database tables exist

---

## **💰 Cost Breakdown**

### **Free Tiers:**
- **Vercel:** Free for personal projects
- **Railway:** $5/month after free trial
- **Supabase:** Free tier (500MB database)
- **OpenAI:** Pay-per-use (~$0.002 per flow generation)

### **Total Monthly Cost: ~$5-10**
