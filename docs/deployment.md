# SmartDine — Deployment Guide

> **Backend** → [Railway](https://railway.app) | **Frontend** → [Vercel](https://vercel.com)

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Pre-Deployment Checklist](#2-pre-deployment-checklist)
3. [Step 1 — Code Changes Required](#3-step-1--code-changes-required)
4. [Step 2 — Deploy Backend on Railway](#4-step-2--deploy-backend-on-railway)
5. [Step 3 — Deploy Frontend on Vercel](#5-step-3--deploy-frontend-on-vercel)
6. [Step 4 — Connect Frontend ↔ Backend](#6-step-4--connect-frontend--backend)
7. [Environment Variables Reference](#7-environment-variables-reference)
8. [Post-Deployment Verification](#8-post-deployment-verification)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Architecture Overview

```
User Browser
     │
     ▼
┌─────────────────────┐
│  Vercel (Frontend)  │  React + Vite (static build)
│  your-app.vercel.app│
└─────────┬───────────┘
          │ HTTPS POST /api/v1/recommend
          ▼
┌─────────────────────┐
│  Railway (Backend)  │  FastAPI + Uvicorn
│  your-app.railway.  │  Loads HuggingFace dataset on startup
│  app                │  Calls Groq LLM API
└─────────────────────┘
          │
          ▼
    Groq Cloud API
    (llama-3.3-70b-versatile)
```

**Key notes:**
- The dataset (`ManikaSaini/zomato-restaurant-recommendation`) is downloaded from HuggingFace **at runtime** on Railway startup — no file uploads needed.
- The in-memory LRU cache (`src/core/cache.py`) is **per-instance** and will reset on Railway restarts/redeploys.
- Railway's free tier sleeps after inactivity; the first request after sleep will be slow (~30–60s) due to dataset reload.

---

## 2. Pre-Deployment Checklist

- [ ] You have a [Railway account](https://railway.app) (free tier works)
- [ ] You have a [Vercel account](https://vercel.com) (free tier works)
- [ ] Your code is pushed to a GitHub repository
- [ ] You have your **Groq API key** — get one free at [console.groq.com](https://console.groq.com)
- [ ] The `pre-main` branch is clean and ready to deploy

---

## 3. Step 1 — Code Changes Required

> [!IMPORTANT]
> **Two code changes are mandatory before deploying.** Without them, the frontend will fail to reach the backend in production.

### 3.1 — Add a `Procfile` for Railway

Railway needs to know how to start the FastAPI server. Create a `Procfile` in the **project root** (alongside `requirements.txt`):

```
web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

> Railway injects the `$PORT` environment variable automatically. You **must** bind to `0.0.0.0` and `$PORT` — not hardcoded `8000`.

### 3.2 — Update CORS via Environment Variable (already done in code)

The CORS middleware in `src/main.py` now reads a `FRONTEND_URL` environment variable at startup and adds it to the allowed origins list. **No code edit is needed** — just set this variable in Railway after you have your Vercel URL (Step 4.6 below).

```python
# How it works in src/main.py (already implemented):
_frontend_url = os.getenv("FRONTEND_URL", "").strip()
if _frontend_url:
    _cors_origins.append(_frontend_url)
```

### 3.3 — Update the API base URL in `frontend/src/api/client.js`

The frontend currently uses a relative path (`/api/v1`) which worked because Vite's dev proxy forwarded it to `localhost:8000`. **On Vercel there is no proxy** — the request must go directly to the Railway URL.

Replace the top of `frontend/src/api/client.js`:

```js
// Before (local dev only):
const API_BASE = "/api/v1";

// After (production-aware):
const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1";  // fallback keeps local dev working
```

You will set `VITE_API_URL` as a Vercel environment variable in Step 3 (it will be your Railway backend URL).

### 3.4 — Commit and Push

```bash
git add Procfile src/main.py frontend/src/api/client.js
git commit -m "chore: add Procfile and production API URL support"
git push origin pre-main
```

---

## 4. Step 2 — Deploy Backend on Railway

### 4.1 — Create a New Railway Project

1. Go to [railway.app](https://railway.app) → **New Project**
2. Select **Deploy from GitHub repo**
3. Connect your GitHub account if prompted
4. Select your `SmartDine` repository and the `pre-main` branch

### 4.2 — Configure the Service

After Railway detects the repo:

1. Click on the created service → **Settings** tab
2. Under **Source**, confirm the **Branch** is set to `pre-main`
3. Under **Build**, set the **Root Directory** to `/` (project root — where `requirements.txt` lives)
4. Railway auto-detects Python and will run `pip install -r requirements.txt`

### 4.3 — Set Environment Variables

Go to your service → **Variables** tab → add the following:

| Variable | Value | Required |
|---|---|---|
| `GROQ_API_KEY` | `gsk_xxxxxxxxxxxxxxxxxxxx` | ✅ Yes |
| `LLM_MODEL` | `llama-3.3-70b-versatile` | Optional |
| `LLM_TEMPERATURE` | `0.3` | Optional |
| `BUDGET_LOW_MAX` | `300` | Optional |
| `BUDGET_MEDIUM_MAX` | `800` | Optional |
| `MAX_CANDIDATES` | `20` | Optional |
| `LOG_LEVEL` | `INFO` | Optional |

> [!CAUTION]
> Never commit your `GROQ_API_KEY` to git. Railway's Variables tab is the correct place — they are injected as environment variables at runtime and never exposed in the build logs.

### 4.4 — Deploy

1. Click **Deploy** (or push a commit — Railway auto-deploys on push)
2. Watch the **Deployment Logs** — look for:
   ```
   SmartDine API starting — loading dataset...
   Dataset ready: XXXX restaurants in memory
   ```
3. Once healthy, click **Settings** → **Networking** → **Generate Domain**
4. Your backend URL will look like: `https://smartdine-production-xxxx.up.railway.app`

> [!NOTE]
> The first deploy takes **3–5 minutes** because Railway downloads and installs all Python dependencies and then downloads the ~50MB HuggingFace dataset. Subsequent deploys are faster due to build caching.

### 4.5 — Verify the Backend

Open a browser or use `curl`:

```bash
curl https://smartdine-production-xxxx.up.railway.app/health
```

Expected response:
```json
{"status": "ok", "restaurants_loaded": 9002}
```

You can also visit the interactive API docs at:
```
https://smartdine-production-xxxx.up.railway.app/docs
```

---

## 5. Step 3 — Deploy Frontend on Vercel

### 5.1 — Import the Project

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Select **Import Git Repository** → connect GitHub → select `SmartDine`
3. Vercel will auto-detect it as a Vite project

### 5.2 — Configure Build Settings

| Setting | Value |
|---|---|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |
| **Install Command** | `npm install` |

> [!IMPORTANT]
> Set the **Root Directory** to `frontend` — this is the most common mistake. Vercel must look inside the `frontend/` folder, not the project root.

### 5.3 — Set Environment Variables

Under **Environment Variables** (before first deploy):

| Variable | Value |
|---|---|
| `VITE_API_URL` | `https://smartdine-production-xxxx.up.railway.app` |

Replace `smartdine-production-xxxx.up.railway.app` with your actual Railway URL from Step 4.4.

> [!NOTE]
> Vite bakes `VITE_*` variables into the static bundle at **build time** — they are not injected at runtime. After changing `VITE_API_URL`, you must **redeploy** (trigger a new build) for the change to take effect.

### 5.4 — Deploy

1. Click **Deploy**
2. Vercel runs `npm install` then `npm run build` inside the `frontend/` directory
3. Once complete, your app is live at: `https://your-app-name.vercel.app`

---

## 6. Step 4 — Connect Frontend ↔ Backend

### 6.1 — Set `FRONTEND_URL` on Railway

Now that you have your Vercel URL, go to Railway → your service → **Variables** tab and add:

| Variable | Value |
|---|---|
| `FRONTEND_URL` | `https://your-app-name.vercel.app` |

Then click **Redeploy**. The backend reads this env var at startup and adds it to the CORS allowed origins list. **No code changes needed.**

### 6.2 — Add a `vercel.json` for SPA Routing (Optional but Recommended)

If your frontend uses client-side routing and you want deep links to work (e.g., `/results`), create `frontend/vercel.json`:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 7. Environment Variables Reference

### Backend (Railway)

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | **Required.** Your Groq API key |
| `FRONTEND_URL` | — | **Required for CORS.** Your Vercel URL, e.g. `https://your-app.vercel.app` |
| `LLM_MODEL` | `llama-3.3-70b-versatile` | Groq model to use |
| `LLM_TEMPERATURE` | `0.3` | Generation temperature (0.0–2.0) |
| `BUDGET_LOW_MAX` | `300` | Max INR cost classified as "low" budget |
| `BUDGET_MEDIUM_MAX` | `800` | Max INR cost classified as "medium" budget |
| `MAX_CANDIDATES` | `20` | Max restaurant rows passed to LLM per request |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `PORT` | (set by Railway) | Do not set manually — Railway injects this |

### Frontend (Vercel)

| Variable | Description |
|---|---|
| `VITE_API_URL` | Full Railway backend URL, no trailing slash. E.g. `https://smartdine-xxxx.up.railway.app` |

---

## 8. Post-Deployment Verification

Run through this checklist after both services are live:

- [ ] `GET /health` on Railway returns `{"status": "ok", "restaurants_loaded": 9002}`
- [ ] `GET /docs` on Railway shows the Swagger UI with the `/api/v1/recommend` endpoint
- [ ] Vercel frontend loads without console errors
- [ ] Submitting a recommendation form returns results (check Network tab — the request should go to your Railway URL)
- [ ] Check Railway logs for any `CRITICAL` or `ERROR` messages

### Quick Smoke Test via curl

```bash
curl -X POST https://smartdine-production-xxxx.up.railway.app/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Bangalore",
    "budget": "medium",
    "cuisine": "North Indian",
    "min_rating": 4.0,
    "top_n": 3
  }'
```

Expected: a JSON response with `recommendations` and `query_metadata`.

---

## 9. Troubleshooting

### Backend (Railway)

| Symptom | Cause | Fix |
|---|---|---|
| Deploy fails with `CONFIGURATION ERROR: GROQ_API_KEY is missing` | `GROQ_API_KEY` not set in Railway Variables | Add the variable in Railway → Variables tab |
| Deploy fails with `RuntimeError: Failed to load dataset` | HuggingFace is unreachable or rate-limited | Retry the deploy; Railway has outbound internet access |
| `uvicorn: command not found` | `Procfile` missing or incorrect | Ensure `Procfile` is in the project root with `web: uvicorn src.main:app --host 0.0.0.0 --port $PORT` |
| 500 error on `/api/v1/recommend` | Dataset didn't load | Check Railway logs for `CRITICAL` messages |
| Deployment hangs indefinitely | Railway can't find the start command | Verify `Procfile` exists at repo root and is committed |

### Frontend (Vercel)

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot connect to the backend` error in UI | `VITE_API_URL` not set or wrong | Check Vercel → Project → Settings → Environment Variables |
| CORS error in browser console | Railway CORS list doesn't include your Vercel domain | Update `allow_origins` in `src/main.py`, push, redeploy Railway |
| Build fails: `Cannot find module` | Root Directory not set to `frontend` | Vercel → Project → Settings → General → Root Directory → `frontend` |
| `VITE_API_URL` changes not reflecting | Vite bakes env vars at build time | Trigger a new Vercel deploy after updating the variable |
| Blank page on direct URL access | Missing SPA rewrite rule | Add `vercel.json` with rewrite rule (see Section 6.2) |

### Local Development (still works as before)

```bash
# Terminal 1 — Backend
cd c:\Users\panka\Documents\Pankaj_CodeSpace\AI_Projects\SmartDine
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
# Visit http://localhost:5173 — Vite proxy forwards /api → localhost:8000
```

---

*Last updated: 2026-06-22 | Branch: `pre-main`*
