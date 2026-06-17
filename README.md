# SmartDine 🍽️

SmartDine is an AI-powered restaurant recommendation system inspired by Zomato. It combines structured restaurant data (loaded from the Hugging Face `ManikaSaini/zomato-restaurant-recommendation` dataset) with a Large Language Model (LLM) to deliver highly personalized, human-readable dining recommendations with clear natural language reasoning.

---

## Key Features

- **Personalized Filter Engine**: Multi-stage cascaded filtering on location, budget, cuisine, and rating to extract optimal candidates.
- **Explainable Recommendations**: Natural language explanations for why each restaurant matches your query, powered by Llama 3.3.
- **Ultra-Fast Free Tier Stack**: Employs Streamlit, FastAPI, and the Groq API (using `llama-3.3-70b-versatile`) for sub-5 second responses.
- **Robust Caching**: Built-in TTL response caching to deliver instant results (<50ms) for repeat queries.

---

## Tech Stack

- **Frontend:** Streamlit
- **Backend API:** FastAPI (Uvicorn ASGI server)
- **Data Layer:** Pandas + Hugging Face `datasets`
- **LLM Engine:** Groq API (`llama-3.3-70b-versatile` / `llama3-8b-8192`)
- **Validation:** Pydantic v2
- **Caching:** Cachetools (In-memory TTL)
- **Testing:** Pytest + Pytest-Asyncio

---

## Installation & Setup

Detailed instructions will be added as implementation progresses. Please see the [implementation plan](docs/implementation-plan.md) and [architecture design](docs/architecture.md) for details on the development roadmap.

## Start backend server
.venv/Scripts/uvicorn src.main:app --port 8000
