# Deployment Guide - Chess King & Pawn Game

Complete guide to deploy your chess game with hybrid architecture: Cloudflare Pages (frontend) + Render.com (backend).

## Architecture Overview

```
Frontend (Static Files) → Cloudflare Pages (Free)
                    ↓
Backend (Python Flask) → Render.com (Free Tier)
                    ↓
Database (SQLite) → Render.com Storage
```

## Prerequisites

- GitHub account with project repository
- Render.com account (free tier)
- Cloudflare account (free tier)
- Git installed locally

## Step 1: Prepare Your Repository

### 1.1 Push Code to GitHub

```bash
# Initialize git if not already done
cd chess-king-pawn
git init
git add .
git commit -m "Initial commit - Chess game backend and frontend"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/chess-king-pawn.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Repository Structure

Your repository should have:
- `/backend` - Flask application
- `/frontend` - Static HTML/CSS/JS files
- `README.md` - Project documentation

## Step 2: Deploy Backend to Render.com

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repository

### 2.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your `chess-king-pawn` repository
3. Configure settings:

```yaml
Name: chess-backend
Environment: Python 3
Region: Oregon (us-west) or closest to you
Branch: main
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn wsgi:app
```

### 2.3 Configure Environment Variables

Add these environment variables in Render dashboard:

```bash
FLASK_ENV=production
SECRET_KEY=generate-a-secure-random-key-here
FRONTEND_URLS=https://chess-king-pawn.pages.dev,https://your-custom-domain.com
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Deploy

- Click **"Create Web Service"**
- Wait for deployment (2-3 minutes)
- Render will provide a URL like: `https://chess-backend.onrender.com`

**Save your backend URL!** You'll need it for the frontend configuration.

### 2.5 Test Backend Deployment

```bash
# Test health endpoint
curl https://chess-backend.onrender.com/api/health

# Expected response:
# {"status":"healthy","message":"Chess API is running"}
```

## Step 3: Deploy Frontend to Cloudflare Pages

### 3.1 Create Cloudflare Account

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com/)
2. Sign up for free account
3. Go to **"Workers & Pages"**

### 3.2 Create Pages Project

1. Click **"Create application"** → **"Pages"** → **"Connect to Git"**
2. Select your GitHub repository
3. Configure build settings:

```bash
Project name: chess-king-pawn
Production branch: main
Build command: (leave empty for static files)
Build output directory: frontend
Root directory: (leave empty)
```

### 3.3 Configure Environment Variables

Add environment variable:

```bash
VITE_API_URL=https://chess-backend.onrender.com/api
```

### 3.4 Deploy

- Click **"Save and Deploy"**
- Cloudflare will provide URL: `https://chess-king-pawn.pages.dev`

**Save your frontend URL!**

### 3.5 Update Frontend API Configuration

Edit `frontend/js/api.js` to use production URL:

```javascript
// Change this line:
constructor(baseURL = 'http://localhost:5000/api') {

// To:
constructor(baseURL = 'https://chess-backend.onrender.com/api') {
```

Or update based on environment:

```javascript
const isProduction = window.location.hostname !== 'localhost';
const apiURL = isProduction
    ? 'https://chess-backend.onrender.com/api'
    : 'http://localhost:5000/api';

class ChessAPI {
    constructor(baseURL = apiURL) {
```

### 3.6 Commit and Push Changes

```bash
git add frontend/js/api.js
git commit -m "Update API URL for production"
git push origin main
```

Cloudflare will automatically redeploy with the changes.

## Step 4: Configure CORS

### 4.1 Update Render Environment Variables

Go to your Render service dashboard and add your frontend URL:

```bash
FRONTEND_URLS=https://chess-king-pawn.pages.dev,http://localhost:5500
```

### 4.2 Test CORS

```bash
# Test from browser console on your frontend
fetch('https://chess-backend.onrender.com/api/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(console.log)
```

## Step 5: Custom Domain (Optional)

### 5.1 Cloudflare Pages Custom Domain

1. Go to your Pages project in Cloudflare dashboard
2. Click **"Custom domains"** → **"Set up a custom domain"**
3. Enter your domain (e.g., `chess.yourdomain.com`)
4. Follow DNS instructions

### 5.2 Update CORS Configuration

Add your custom domain to Render environment variables:

```bash
FRONTEND_URLS=https://chess-king-pawn.pages.dev,https://chess.yourdomain.com,http://localhost:5500
```

## Step 6: Final Testing

### 6.1 Test Complete Flow

1. Visit your frontend URL
2. Register/login with username
3. Start a new game
4. Make a move
5. Verify bot responds
6. Test settings persistence
7. Test theme switching
8. Test timer functionality

### 6.2 Monitor Deployments

**Render.com:**
- Dashboard shows real-time logs
- Metrics for response time, CPU, memory
- Auto-deploys on git push

**Cloudflare Pages:**
- Analytics for traffic and performance
- Preview deployments for each commit
- Global CDN distribution

## Step 7: Security Best Practices

### 7.1 Environment Variables

Never commit secrets to git! Use environment variables:

```bash
# Required
SECRET_KEY=your-secret-key
FRONTEND_URLS=your-frontend-url

# Optional
DATABASE_URL=production-database-url
```

### 7.2 Production Checklist

- ✅ Strong SECRET_KEY (generate with Python)
- ✅ HTTPS enabled (automatic on Cloudflare/Render)
- ✅ CORS configured correctly
- ✅ Error messages don't leak sensitive info
- ✅ Rate limiting (consider adding)
- ✅ Input validation (already implemented)

## Troubleshooting

### Backend Issues

**Service not starting:**
```bash
# Check Render logs
# Verify requirements.txt has all dependencies
# Ensure wsgi.py exists and is correct
```

**Database errors:**
```bash
# SQLite will be created automatically
# For production, consider PostgreSQL:
# Add DATABASE_URL environment variable
```

### Frontend Issues

**CORS errors:**
```bash
# Verify FRONTEND_URLS includes your frontend domain
# Check browser console for specific error
# Test API endpoint directly
```

**API not responding:**
```bash
# Check backend deployment status on Render
# Verify API URL in frontend code
# Test backend health endpoint
```

### Deployment Issues

**Build failures:**
```bash
# Check build logs on Render/Cloudflare
# Verify file structure is correct
# Ensure all files are committed to git
```

## Maintenance

### Updates

```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push origin main

# Both platforms auto-deploy
# Render: 2-3 minutes
# Cloudflare: 1-2 minutes
```

### Monitoring

- **Render**: Dashboard shows logs and metrics
- **Cloudflare**: Analytics for performance
- **GitHub**: Issues for bug tracking

## Costs

### Free Tier Limits

**Render.com:**
- 750 hours/month free
- Sufficient for hobby projects
- Auto-suspension after inactivity

**Cloudflare Pages:**
- Unlimited bandwidth
- Unlimited requests
- 500 builds per month

**Total Cost: $0/month** 🎉

## Next Steps

1. ✅ Deploy to production
2. ✅ Test all functionality
3. ✅ Share with friends!
4. 📝 Monitor usage
5. 🚀 Add features as needed

## Support

- **Render**: [render.com/docs](https://render.com/docs)
- **Cloudflare**: [developers.cloudflare.com/pages](https://developers.cloudflare.com/pages)
- **GitHub**: Check repository issues

---

**Congratulations!** Your chess game is now live and accessible to players worldwide! 🎮
