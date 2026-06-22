# SmartDine 🍽️

SmartDine is an AI-powered restaurant recommendation system inspired by Zomato. It combines structured restaurant data (loaded from the Hugging Face `ManikaSaini/zomato-restaurant-recommendation` dataset) with a Large Language Model (LLM) to deliver highly personalized, human-readable dining recommendations with clear natural language reasoning.

---

## Project Overview

SmartDine uses a multi-stage cascaded filtering engine on location, budget, cuisine, and rating to extract optimal candidates. The candidates are then passed to an LLM (powered by Llama 3.3) which generates natural language explanations for why each restaurant matches your query. 

It features an ultra-fast free tier stack ensuring sub-5 second responses, and built-in TTL response caching to deliver instant results (<50ms) for repeat queries.

---

## Tech Stack

| Layer | Technology | Free? |
|---|---|---|
| Frontend | Vite + React + react-icons | ✅ |
| Backend API | FastAPI + Uvicorn | ✅ |
| Data Loading | HF `datasets` | ✅ |
| Data Processing | Pandas | ✅ |
| LLM Provider | Groq API (Llama 3.3 70B) | ✅ (no CC) |
| LLM SDK | `groq` Python package | ✅ |
| Validation | Pydantic v2 | ✅ |
| Config | `pydantic-settings` + `python-dotenv` | ✅ |
| Retry Logic | `tenacity` | ✅ |
| Caching | `cachetools` (in-memory TTL) | ✅ |
| Testing | `pytest` + `pytest-asyncio` | ✅ |

---

## Prerequisites

- **Python 3.10+**
- **Node.js (v18+)** and npm
- **Groq API Key**: Get your FREE Groq API key at [console.groq.com](https://console.groq.com/) (no credit card needed).

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Pankaj-Shrivastava/SmartDine.git
   cd SmartDine
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Configure Environment Variables:**
   Copy the example config and add your API key:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set `GROQ_API_KEY=your_groq_api_key_here`.

---

## Running the App

Run the backend and frontend simultaneously in two separate terminals:

**Terminal 1 — Start the FastAPI backend:**
```bash
cd SmartDine
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 — Start the React frontend:**
```bash
cd SmartDine/frontend
npm run dev
```

The application will be available at `http://localhost:5173`.

---

## API Reference

### `POST /api/v1/recommend`
Fetches personalized restaurant recommendations.

**Request Schema:**
```json
{
  "location": "Koramangala",
  "budget": "medium",
  "cuisine": "Italian",
  "min_rating": 3.5,
  "extras": "family-friendly",
  "top_n": 5
}
```

**Response Schema:**
```json
{
  "recommendations": [
    {
      "rank": 1,
      "name": "Restaurant Name",
      "cuisine": "Italian",
      "rating": 4.5,
      "cost_for_two": 600,
      "explanation": "One-paragraph AI explanation."
    }
  ],
  "query_metadata": {
    "location": "Koramangala",
    "budget": "medium",
    "cuisine": "Italian",
    "min_rating": 3.5,
    "top_n": 5,
    "candidates_found": 10
  }
}
```

### `GET /health`
Returns the health status of the API and the number of loaded restaurants.

---

## Project Structure

```text
SmartDine/
├── docs/                 # Architecture and planning documentation
├── frontend/             # Vite + React SPA
│   ├── src/              # React components, hooks, API client
│   └── package.json      # Node dependencies
├── src/                  # FastAPI backend
│   ├── api/              # API routes and Pydantic schemas
│   ├── core/             # Filter engine, LLM client, Prompt builder
│   ├── data/             # Dataset loading and cleaning
│   ├── config.py         # App configuration settings
│   └── main.py           # FastAPI entry point
├── tests/                # Pytest unit and integration tests
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Limitations & Roadmap

For detailed limitations, future scalability plans, and technical architecture details, please refer to [Section 6 of the Architecture Document](./docs/architecture.md).
