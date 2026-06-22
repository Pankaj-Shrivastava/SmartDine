# SmartDine — Implementation Plan

> **Version:** 1.0
> **Last Updated:** 2026-06-14
> **Status:** Active Development Roadmap
> **Sources:** [`context.md`](./context.md) · [`architecture.md`](./architecture.md)

---

## Overview

This document is the step-by-step development roadmap for **SmartDine**, an AI-powered restaurant recommendation system. The system combines a pre-filtered Pandas DataFrame (Zomato dataset from Hugging Face) with the Groq LLM API (free tier) to deliver personalized, explainable dining recommendations via a Streamlit frontend and a FastAPI backend.

The implementation is divided into **6 sequential phases**. Each phase must be fully completed and verified against its Acceptance Criteria before the next phase begins.

---

## Phase Summary

| Phase | Name | Focus | Est. Effort |
|---|---|---|---|
| **Phase 0** | Setup | Repo, environment, dependencies, folder structure | ~1 hour |
| **Phase 1** | Data | Dataset ingestion, cleaning, in-memory DataFrame | ~2 hours |
| **Phase 2** | Filter | Filter engine, validation layer, FastAPI skeleton | ~3 hours |
| **Phase 3** | LLM | Prompt engineering, Groq API integration, response parsing | ~3 hours |
| **Phase 4** | UI | Vite + React SPA, component architecture, react-icons, dark theme | ~4 hours |
| **Phase 5** | Hardening | Error handling, caching, testing, documentation | ~3 hours |

---

## Phase 0 — Setup

### Objective

Establish a clean, reproducible development environment. Create the complete folder structure defined in Appendix A of `architecture.md`, install all core dependencies, and configure environment variables. After this phase, every teammate should be able to clone the repo and run the app with one command.

---

### Key Tasks

#### 0.1 Repository & Version Control

- [ ] Confirm Git repository is initialised at `SmartDine/` on `main` branch
- [ ] Create `.gitignore` with entries for: `.env`, `__pycache__/`, `.venv/`, `*.pyc`, `*.egg-info/`, `.pytest_cache/`, `dist/`
- [ ] Create `README.md` with project title, brief description, tech stack badge list, and placeholder sections for: Installation, Usage, Environment Variables, and Contributing

#### 0.2 Virtual Environment

- [ ] Create a Python virtual environment: `python -m venv .venv`
- [ ] Activate the environment (Windows: `.venv\Scripts\activate`)
- [ ] Verify Python version ≥ 3.10: `python --version`

#### 0.3 Dependencies

- [ ] Create `requirements.txt` with the following pinned packages:

```text
# Data
pandas>=2.1.0
datasets>=2.18.0

# Backend
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.1

# LLM
groq>=0.9.0
tenacity>=8.3.0

# Frontend (React — managed via npm in frontend/package.json)
# No Python dependencies needed for the frontend

# Utilities
cachetools>=5.3.3
httpx>=0.27.0         # async HTTP client used internally

# Testing
pytest>=8.2.0
pytest-asyncio>=0.23.0
httpx>=0.27.0         # also used by TestClient
```

- [ ] Install all dependencies: `pip install -r requirements.txt`
- [ ] Verify installation: `pip list | findstr -i "fastapi groq streamlit pandas"`

#### 0.4 Folder Structure

- [ ] Create the complete project structure from Appendix A of `architecture.md`:

```
SmartDine/
├── docs/
│   ├── problemStatement.txt       ✅ (exists)
│   ├── context.md                 ✅ (exists)
│   ├── architecture.md            ✅ (exists)
│   └── implementation-plan.md     ✅ (this document)
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entrypoint
│   ├── config.py                  # Settings (env vars, budget thresholds)
│   ├── data/
│   │   ├── __init__.py
│   │   └── ingestion.py           # Dataset loading & cleaning
│   ├── core/
│   │   ├── __init__.py
│   │   ├── filter_engine.py       # Pandas-based filtering logic
│   │   ├── prompt_builder.py      # Prompt template construction
│   │   └── llm_client.py          # Groq API client with retries
│   └── api/
│       ├── __init__.py
│       ├── routes.py              # API route definitions
│       └── schemas.py             # Pydantic request/response models
├── frontend/
│   ├── index.html                 # React app entry point
│   ├── package.json               # npm dependencies (react, react-icons)
│   ├── vite.config.js             # Vite dev server + API proxy config
│   └── src/                       # React components, hooks, API client
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_filter_engine.py
│   ├── test_prompt_builder.py
│   └── test_api.py
├── .env.example
├── .env                           # (git-ignored — local secrets only)
├── .gitignore
├── requirements.txt
└── README.md
```

- [ ] Create all empty `__init__.py` files for each Python package directory
- [ ] Verify structure with: `tree /f /a` (Windows) or `find . -type f` (Unix)

#### 0.5 Environment Variables

- [ ] Create `.env.example` with all variables from Appendix B of `architecture.md`:

```dotenv
# ─── REQUIRED ─────────────────────────────────────────────────────────────────
# Get your FREE Groq API key at: https://console.groq.com/ (no credit card needed)
GROQ_API_KEY=your_groq_api_key_here

# ─── OPTIONAL OVERRIDES ────────────────────────────────────────────────────────
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.3

# Budget thresholds (INR for two people)
BUDGET_LOW_MAX=300
BUDGET_MEDIUM_MAX=800

# Maximum candidate rows sent to the LLM per request
MAX_CANDIDATES=20

# Logging
LOG_LEVEL=INFO
```

- [ ] Copy `.env.example` → `.env` and fill in your personal `GROQ_API_KEY`
- [ ] Sign up at [console.groq.com](https://console.groq.com/) to get your free API key if you don't have one

#### 0.6 Configuration Module

- [ ] Create `src/config.py` to centralise all settings:

```python
# src/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    groq_api_key: str
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.3
    budget_low_max: int = 300
    budget_medium_max: int = 800
    max_candidates: int = 20
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

### Dependencies

> None — this is the first phase.

---

### Acceptance Criteria

- [ ] `python -c "import fastapi, groq, streamlit, pandas, datasets; print('OK')"` runs without errors
- [ ] All directories and `__init__.py` files exist as per the folder structure above
- [ ] `.env` is present locally and contains a valid `GROQ_API_KEY`; `.env` is listed in `.gitignore`
- [ ] `.env.example` is committed to Git with placeholder values
- [ ] `python -c "from src.config import get_settings; s = get_settings(); print(s.llm_model)"` prints `llama-3.3-70b-versatile`

---

## Phase 1 — Data

### Objective

Load the Zomato restaurant dataset from Hugging Face into memory, apply all necessary cleaning transformations (parse ratings, costs, normalise text), and expose a stable, typed DataFrame that all downstream modules can depend on. Data quality issues are resolved at load time — zero per-request overhead.

---

### Key Tasks

#### 1.1 Dataset Ingestion

- [ ] Implement `src/data/ingestion.py` with the `load_and_clean()` function:
  - Load `ManikaSaini/zomato-restaurant-recommendation` using `datasets.load_dataset(split="train")`
  - Convert HF dataset to Pandas DataFrame via `.to_pandas()`
  - Drop duplicate rows keyed on `["name", "location"]`
  - **Parse `rate` column:** extract numeric value from strings like `"4.1/5"` using regex `(\d+\.?\d*)`; handle `"NEW"`, `"-"`, and `NaN` by coercing to `NaN`; store in new column `rating` (float)
  - **Parse `approx_cost(for two people)` column:** remove commas, cast to float; store in new column `cost` (float)
  - **Normalise `cuisines`:** lowercase + strip whitespace; store in new column `cuisines_clean`
  - Drop rows where `name`, `location`, `rating`, or `cost` are `NaN`
  - Return cleaned `pd.DataFrame`

```python
# Skeleton — src/data/ingestion.py
import pandas as pd
from datasets import load_dataset
import logging

logger = logging.getLogger(__name__)

def load_and_clean() -> pd.DataFrame:
    """Load the Zomato HF dataset and return a cleaned DataFrame."""
    logger.info("Loading dataset from Hugging Face...")
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = ds.to_pandas()
    logger.info(f"Raw dataset: {len(df)} rows, {len(df.columns)} columns")

    # De-duplicate
    df = df.drop_duplicates(subset=["name", "location"])

    # Parse rating: "4.1/5" → 4.1
    df["rating"] = (
        df["rate"]
        .str.extract(r"(\d+\.?\d*)")
        .astype(float)
    )

    # Parse cost: "1,200" → 1200.0
    df["cost"] = (
        df["approx_cost(for two people)"]
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )

    # Normalise cuisines
    df["cuisines_clean"] = df["cuisines"].str.lower().str.strip()

    # Drop rows with critical nulls
    before = len(df)
    df = df.dropna(subset=["name", "location", "rating", "cost"])
    logger.info(f"After cleaning: {len(df)} rows (dropped {before - len(df)} rows)")

    return df.reset_index(drop=True)
```

#### 1.2 Singleton DataFrame at Startup

- [ ] Create `src/main.py` — FastAPI entrypoint — with a `lifespan` context manager that loads the dataset **once** at startup and stores it as an `app.state` attribute:

```python
# src/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.data.ingestion import load_and_clean
from src.config import get_settings
from src.api.routes import router

logging.basicConfig(level=get_settings().log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SmartDine API starting — loading dataset...")
    app.state.df = load_and_clean()
    logger.info(f"Dataset ready: {len(app.state.df)} restaurants in memory")
    yield
    logger.info("SmartDine API shutting down")

app = FastAPI(
    title="SmartDine API",
    description="AI-Powered Restaurant Recommendation System",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "restaurants_loaded": len(app.state.df)}
```

#### 1.3 Data Quality Validation

- [ ] After loading, log and assert the following data quality checks (raise `RuntimeError` if any fail):
  - Total row count > 10,000 (sanity check that the dataset loaded correctly)
  - `rating` column: 0 < values ≤ 5.0 (no out-of-range ratings)
  - `cost` column: all values > 0
  - No nulls in `["name", "location", "cuisines_clean"]`

#### 1.4 Unit Tests — Data

- [ ] Create `tests/test_ingestion.py`:
  - `test_dataframe_not_empty()` — assert `len(df) > 0`
  - `test_rating_column_type()` — assert `df["rating"].dtype == float`
  - `test_cost_column_type()` — assert `df["cost"].dtype == float`
  - `test_no_critical_nulls()` — assert zero nulls in `name`, `location`, `rating`, `cost`
  - `test_rating_range()` — assert all ratings are in range `(0, 5]`
  - `test_cuisines_normalised()` — assert `df["cuisines_clean"]` is all lowercase

---

### Dependencies

> Phase 0 must be complete. Virtual environment active, `requirements.txt` installed.

---

### Acceptance Criteria

- [ ] `python -c "from src.data.ingestion import load_and_clean; df = load_and_clean(); print(df.shape)"` prints a shape with > 10,000 rows
- [ ] `df["rating"]` contains only floats in range `(0.0, 5.0]` with no NaN values
- [ ] `df["cost"]` contains only positive floats with no NaN values
- [ ] `pytest tests/test_ingestion.py -v` — **all tests pass**
- [ ] Running `uvicorn src.main:app --reload` and calling `GET /health` returns `{"status": "ok", "restaurants_loaded": <N>}` where N > 10,000

---

## Phase 2 — Filter

### Objective

Build the Data Filter Engine — the critical optimisation layer that reduces ~51K restaurant rows to ≤ 20 highly relevant candidates before any LLM call. Implement input validation and normalisation via Pydantic schemas, the cascaded filter logic with progressive fallback, and expose a working `POST /api/v1/recommend` endpoint that returns the raw filtered DataFrame (LLM integration comes in Phase 3).

---

### Key Tasks

#### 2.1 Pydantic Schemas

- [ ] Create `src/api/schemas.py` with all request and response models:

```python
# src/api/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class RecommendationRequest(BaseModel):
    location: str = Field(..., min_length=2, example="Koramangala",
                          description="Neighbourhood or city area name")
    budget: Literal["low", "medium", "high"] = Field(...,
                    description="low (≤₹300) | medium (₹301–₹800) | high (₹801+)")
    cuisine: Optional[str] = Field(None, example="Italian",
                                   description="Preferred cuisine type (optional)")
    min_rating: float = Field(3.5, ge=0.0, le=5.0,
                              description="Minimum acceptable rating (0.0–5.0)")
    extras: Optional[str] = Field(None, example="family-friendly, table booking",
                                  description="Free-text additional preferences")
    top_n: int = Field(5, ge=1, le=10,
                       description="Number of recommendations to return (1–10)")

class Recommendation(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    cost_for_two: int
    explanation: str

class QueryMetadata(BaseModel):
    location: str
    budget: str
    cuisine: Optional[str]
    min_rating: float
    top_n: int
    candidates_found: int

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    query_metadata: QueryMetadata
```

#### 2.2 Filter Engine

- [ ] Create `src/core/filter_engine.py` with `filter_restaurants()` implementing **cascaded filtering** with **progressive fallback**:

```python
# src/core/filter_engine.py
import pandas as pd
import logging
from src.api.schemas import RecommendationRequest
from src.config import get_settings

logger = logging.getLogger(__name__)

def _get_budget_range(budget: str) -> tuple[float, float]:
    settings = get_settings()
    return {
        "low":    (0, settings.budget_low_max),
        "medium": (settings.budget_low_max + 1, settings.budget_medium_max),
        "high":   (settings.budget_medium_max + 1, float("inf")),
    }[budget]

def filter_restaurants(df: pd.DataFrame, req: RecommendationRequest) -> pd.DataFrame:
    """Apply cascaded filters. Falls back progressively if results are empty."""
    max_candidates = get_settings().max_candidates

    result = _apply_filters(df, req, use_cuisine=True, strict_location=True)

    # Fallback 1: drop cuisine filter
    if result.empty and req.cuisine:
        logger.warning("No results with cuisine filter — relaxing cuisine constraint")
        result = _apply_filters(df, req, use_cuisine=False, strict_location=True)

    # Fallback 2: widen to city-level location
    if result.empty:
        logger.warning("No results for neighbourhood — widening to city-level location")
        result = _apply_filters(df, req, use_cuisine=False, strict_location=False)

    # Fallback 3: return top-rated regardless of budget/cuisine
    if result.empty:
        logger.warning("No results after all fallbacks — returning top-rated in location")
        result = df[
            df["location"].str.lower().str.contains(req.location.lower(), na=False)
        ]

    if result.empty:
        return pd.DataFrame()

    # Cap and sort
    result = result.sort_values(["rating", "votes"], ascending=[False, False])
    return result.head(max_candidates)

def _apply_filters(
    df: pd.DataFrame,
    req: RecommendationRequest,
    use_cuisine: bool,
    strict_location: bool,
) -> pd.DataFrame:
    res = df.copy()

    # Location filter
    if strict_location:
        res = res[res["location"].str.lower().str.contains(req.location.lower(), na=False)]
    else:
        res = res[res["listed_in(city)"].str.lower().str.contains(req.location.lower(), na=False)]

    # Budget filter
    low, high = _get_budget_range(req.budget)
    res = res[(res["cost"] >= low) & (res["cost"] <= high)]

    # Cuisine filter (optional)
    if use_cuisine and req.cuisine:
        res = res[res["cuisines_clean"].str.contains(req.cuisine.lower(), na=False)]

    # Rating filter
    res = res[res["rating"] >= req.min_rating]

    return res
```

#### 2.3 API Route (Stub)

- [ ] Create `src/api/routes.py` with the `/recommend` endpoint wired to the filter engine. The LLM call is **stubbed** in this phase — return the raw candidate list with placeholder explanations:

```python
# src/api/routes.py
from fastapi import APIRouter, Request, HTTPException
from src.api.schemas import (
    RecommendationRequest, RecommendationResponse,
    Recommendation, QueryMetadata
)
from src.core.filter_engine import filter_restaurants
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: Request, body: RecommendationRequest):
    df = request.app.state.df

    candidates = filter_restaurants(df, body)

    if candidates.empty:
        raise HTTPException(
            status_code=404,
            detail="No restaurants found matching your criteria. Try broadening your filters."
        )

    # --- LLM call will be added in Phase 3 ---
    recommendations = [
        Recommendation(
            rank=i + 1,
            name=row["name"],
            cuisine=row["cuisines"],
            rating=round(float(row["rating"]), 1),
            cost_for_two=int(row["cost"]),
            explanation="[AI explanation coming in Phase 3]",
        )
        for i, (_, row) in enumerate(candidates.head(body.top_n).iterrows())
    ]

    return RecommendationResponse(
        recommendations=recommendations,
        query_metadata=QueryMetadata(
            location=body.location,
            budget=body.budget,
            cuisine=body.cuisine,
            min_rating=body.min_rating,
            top_n=body.top_n,
            candidates_found=len(candidates),
        ),
    )
```

#### 2.4 Unit Tests — Filter Engine

- [ ] Create `tests/test_filter_engine.py`:
  - `test_location_filter()` — request for "Koramangala" returns only Koramangala restaurants
  - `test_budget_filter_low()` — `budget="low"` returns only restaurants with `cost <= 300`
  - `test_budget_filter_medium()` — `budget="medium"` returns `301 ≤ cost ≤ 800`
  - `test_cuisine_filter()` — `cuisine="Italian"` returns restaurants whose `cuisines_clean` contains `"italian"`
  - `test_rating_filter()` — `min_rating=4.0` returns only restaurants with `rating >= 4.0`
  - `test_max_candidates_cap()` — result never exceeds `MAX_CANDIDATES` (20)
  - `test_cuisine_fallback()` — if cuisine filter yields 0 results, fallback returns non-empty DataFrame
  - `test_no_results_returns_empty_df()` — nonsense location returns empty DataFrame (no crash)

#### 2.5 Integration Tests — API

- [ ] Create `tests/test_api.py` with FastAPI `TestClient`:
  - `test_recommend_returns_200()` — valid request returns `200 OK`
  - `test_recommend_schema_valid()` — response body matches `RecommendationResponse` schema
  - `test_invalid_budget_returns_422()` — `budget="very cheap"` returns `422 Unprocessable Entity`
  - `test_missing_location_returns_422()` — missing `location` field returns `422`
  - `test_top_n_respected()` — `top_n=3` returns exactly 3 recommendations
  - `test_unknown_location_returns_404()` — `location="ZZZNonExistentCity"` returns `404`

---

### Dependencies

> Phase 1 must be complete. `app.state.df` must be populated at startup.

---

### Acceptance Criteria

- [ ] `POST /api/v1/recommend` with a valid body returns `200 OK` and a JSON payload matching `RecommendationResponse` schema
- [ ] `POST /api/v1/recommend` with `budget="notvalid"` returns `422 Unprocessable Entity`
- [ ] `POST /api/v1/recommend` with location `"ZZZNonExistentCity"` returns `404 Not Found`
- [ ] The `recommendations` list in the response never exceeds `top_n`; `candidates_found` in `query_metadata` is ≤ 20
- [ ] `pytest tests/test_filter_engine.py tests/test_api.py -v` — **all tests pass**
- [ ] FastAPI auto-generated docs available at `http://localhost:8000/docs` with `/recommend` listed

---

## Phase 3 — LLM

### Objective

Replace the Phase 2 stub explanation with a real Groq LLM call. Implement the Prompt Builder (system + user message templates with Markdown table injection), the async Groq API client with retry logic, and the Pydantic response parser. After this phase, every recommendation comes with an AI-generated, context-aware explanation.

---

### Key Tasks

#### 3.1 Prompt Builder

- [ ] Create `src/core/prompt_builder.py` with two functions: `build_system_prompt()` and `build_user_prompt()`:

```python
# src/core/prompt_builder.py
import pandas as pd
from src.api.schemas import RecommendationRequest

SYSTEM_PROMPT_TEMPLATE = """\
You are SmartDine, an expert restaurant recommendation engine.

You will receive:
1. A user's dining preferences.
2. A table of candidate restaurants (pre-filtered from a larger dataset).

Your task:
- Analyse each candidate against the user's preferences.
- Rank the top {top_n} restaurants.
- For each, provide a concise explanation of WHY it's a good fit.

Respond ONLY with a JSON object in this exact schema:
{{
  "recommendations": [
    {{
      "rank": 1,
      "name": "Restaurant Name",
      "cuisine": "Cuisine Type",
      "rating": 4.5,
      "cost_for_two": 600,
      "explanation": "One-paragraph explanation."
    }}
  ]
}}

Ranking criteria (in order of priority):
1. How well the cuisine matches the user's preference.
2. Rating (higher is better).
3. Cost alignment with stated budget.
4. Relevance of additional preferences (e.g., "family-friendly" → prefer Casual Dining or book_table=Yes).
5. Popularity (vote count).

Do NOT include restaurants that are clearly irrelevant.
Do NOT invent data — use only the provided table.
"""

USER_PROMPT_TEMPLATE = """\
## User Preferences
- Location: {location}
- Budget: {budget} (₹{cost_low}–₹{cost_high} for two)
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Additional Preferences: {extras}

## Candidate Restaurants
{markdown_table}

Please rank the top {top_n} restaurants and explain your reasoning.
"""

def build_system_prompt(top_n: int) -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(top_n=top_n)

def build_user_prompt(req: RecommendationRequest, candidates: pd.DataFrame, cost_low: int, cost_high: int) -> str:
    markdown_table = candidates[
        ["name", "location", "cuisines", "rating", "cost", "rest_type", "book_table", "dish_liked"]
    ].rename(columns={
        "name": "Name",
        "location": "Location",
        "cuisines": "Cuisines",
        "rating": "Rating",
        "cost": "Cost (₹ for 2)",
        "rest_type": "Type",
        "book_table": "Book Table",
        "dish_liked": "Popular Dishes",
    }).to_markdown(index=False)

    return USER_PROMPT_TEMPLATE.format(
        location=req.location,
        budget=req.budget,
        cost_low=cost_low,
        cost_high=cost_high,
        cuisine=req.cuisine or "Any",
        min_rating=req.min_rating,
        extras=req.extras or "None specified",
        markdown_table=markdown_table,
        top_n=req.top_n,
    )
```

- [ ] Add `tabulate` to `requirements.txt` (required by `pandas.DataFrame.to_markdown()`)

#### 3.2 LLM Client

- [ ] Create `src/core/llm_client.py` with the async Groq API client and retry logic:

```python
# src/core/llm_client.py
import json
import logging
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def call_llm(system_prompt: str, user_prompt: str) -> dict:
    """Call Groq API (free tier) and return the parsed JSON response."""
    client = AsyncGroq(api_key=settings.groq_api_key)

    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=settings.llm_temperature,
        max_tokens=1024,
    )

    content = response.choices[0].message.content
    logger.debug(f"LLM raw response ({len(content)} chars): {content[:200]}...")
    return json.loads(content)
```

#### 3.3 Response Parsing & Validation

- [ ] Create `src/core/parser.py` to validate the raw LLM JSON dict against the `RecommendationResponse` schema:

```python
# src/core/parser.py
import logging
from typing import Any
from src.api.schemas import Recommendation, RecommendationResponse, QueryMetadata
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def parse_llm_response(
    raw: dict[str, Any],
    query_metadata: QueryMetadata,
) -> RecommendationResponse:
    """Validate LLM JSON against the RecommendationResponse schema."""
    try:
        recs = [Recommendation(**r) for r in raw["recommendations"]]
        return RecommendationResponse(
            recommendations=recs,
            query_metadata=query_metadata,
        )
    except (KeyError, ValidationError) as e:
        logger.error(f"LLM response parsing failed: {e}")
        raise ValueError(f"Malformed LLM response: {e}") from e
```

#### 3.4 Wire LLM into the API Route

- [ ] Update `src/api/routes.py` to replace the Phase 2 stub with a real LLM call:
  - Import `call_llm`, `build_system_prompt`, `build_user_prompt`, `parse_llm_response`
  - After filtering, call `build_system_prompt(top_n)` and `build_user_prompt(req, candidates, cost_low, cost_high)`
  - `await call_llm(system_prompt, user_prompt)` inside a `try/except`
  - On `ValueError` (parse failure after all retries), fall back to returning the raw filtered candidates with a flag `"explanation": "AI service temporarily unavailable — showing top-rated matches."`
  - Return `parse_llm_response(raw, query_metadata)`

#### 3.5 Unit Tests — Prompt Builder

- [ ] Create `tests/test_prompt_builder.py`:
  - `test_system_prompt_contains_json_schema()` — assert `"recommendations"` appears in the system prompt
  - `test_user_prompt_contains_location()` — assert user's location appears in the user prompt
  - `test_user_prompt_markdown_table()` — assert `|` characters are in the user prompt (Markdown table present)
  - `test_user_prompt_cuisine_any_when_none()` — when `cuisine=None`, prompt contains `"Any"`

---

### Dependencies

> Phase 2 must be complete. `/recommend` endpoint must return valid (stubbed) responses.
> `GROQ_API_KEY` must be set in `.env`.

---

### Acceptance Criteria

- [ ] `POST /api/v1/recommend` with valid input returns a `200 OK` where `recommendations[0].explanation` is a non-empty string **generated by the LLM** (not the stub placeholder)
- [ ] The JSON response strictly conforms to the `RecommendationResponse` Pydantic schema
- [ ] Total API response time (including LLM call) is **under 5 seconds** for `top_n=5`
- [ ] If the Groq API is temporarily unreachable (e.g., wrong key), the endpoint returns `recommendations` with `"AI service temporarily unavailable"` explanations rather than a 500 error
- [ ] `pytest tests/test_prompt_builder.py -v` — **all tests pass**

---

## Phase 4 — UI (Vite + React)

### Objective

Build a premium **Vite + React** single-page application that replaces the Streamlit placeholder. The React SPA consumes the existing FastAPI backend via a Vite dev-server proxy, using a component-based architecture with vanilla CSS, `react-icons` (Ionicons 5) for professional SVG icons, glassmorphism styling, and micro-animations. After this phase, a non-technical user can interact with SmartDine entirely through the browser at `localhost:5173`.

---

### Architecture

```
┌─────────────────────────┐         ┌─────────────────────────┐
│   Vite + React SPA      │  HTTP   │   FastAPI Backend        │
│   localhost:5173         │────────▶│   localhost:8000         │
│                          │  Proxy  │                          │
│   ┌─ App ─────────────┐ │         │   POST /api/v1/recommend │
│   │  Hero              │ │         │   GET  /health           │
│   │  SearchForm        │ │         └─────────────────────────┘
│   │  StatsBar          │ │
│   │  ResultsHeader     │ │
│   │  RecommendationCard│ │
│   │  SkeletonCard      │ │
│   │  EmptyState        │ │
│   │  ErrorBanner       │ │
│   └────────────────────┘ │
└─────────────────────────┘
```

### Frontend File Structure

```
frontend/
├── index.html                     # Entry point — loads React app
├── package.json                   # Dependencies (react, vite, react-icons)
├── vite.config.js                 # Dev server config + API proxy
├── public/
│   └── favicon.ico
├── src/
│   ├── main.jsx                   # ReactDOM.createRoot entry
│   ├── App.jsx                    # Root component — layout orchestrator
│   ├── App.css                    # App-level layout styles
│   ├── index.css                  # Global design tokens, resets, fonts, animations
│   ├── api/
│   │   └── client.js              # Fetch wrapper — calls FastAPI
│   ├── hooks/
│   │   └── useRecommendations.js  # Custom hook — search state + API calls
│   └── components/
│       ├── Hero/
│       │   ├── Hero.jsx
│       │   └── Hero.css
│       ├── SearchForm/
│       │   ├── SearchForm.jsx
│       │   └── SearchForm.css
│       ├── RecommendationCard/
│       │   ├── RecommendationCard.jsx
│       │   └── RecommendationCard.css
│       ├── ResultsHeader/
│       │   ├── ResultsHeader.jsx
│       │   └── ResultsHeader.css
│       ├── StatsBar/
│       │   ├── StatsBar.jsx
│       │   └── StatsBar.css
│       ├── SkeletonCard/
│       │   ├── SkeletonCard.jsx
│       │   └── SkeletonCard.css
│       ├── EmptyState/
│       │   ├── EmptyState.jsx
│       │   └── EmptyState.css
│       └── ErrorBanner/
│           ├── ErrorBanner.jsx
│           └── ErrorBanner.css
```

---

### Key Tasks

#### 4.0 Project Setup

- [ ] Delete `frontend/app.py` (Streamlit placeholder) and `frontend/__pycache__/`
- [ ] Initialise Vite + React project inside `frontend/`:

```bash
cd frontend
npx -y create-vite@latest ./ -- --template react
npm install react-icons
```

- [ ] Configure `vite.config.js` with an API proxy so the React app can call `/api/v1/recommend` as a relative path:

```javascript
// frontend/vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            "/api": {
                target: "http://localhost:8000",
                changeOrigin: true,
            },
        },
    },
});
```

- [ ] Set up `index.html` with proper `<title>`, meta description, and favicon
- [ ] Verify `npm run dev` starts on `localhost:5173`

#### 4.1 Design System (`index.css`)

- [ ] Define CSS custom properties (design tokens) for the entire app:

```css
:root {
    --bg-primary:     #0a0f1c;
    --bg-secondary:   #111827;
    --bg-card:        rgba(255, 255, 255, 0.04);
    --bg-card-hover:  rgba(255, 255, 255, 0.08);
    --accent:         #e94560;
    --accent-soft:    rgba(233, 69, 96, 0.15);
    --blue:           #4a9eff;
    --green:          #50c878;
    --gold:           #f0c040;
    --text-primary:   #e8ecf1;
    --text-secondary: #8892a4;
    --text-muted:     #5a6478;
    --border:         rgba(255, 255, 255, 0.08);
    --border-hover:   rgba(233, 69, 96, 0.4);
    --radius-sm:      8px;
    --radius-md:      12px;
    --radius-lg:      16px;
    --radius-xl:      24px;
    --shadow-glow:    0 8px 32px rgba(233, 69, 96, 0.1);
    --font:           'Inter', sans-serif;
    --transition:     all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

- [ ] Import Google Fonts (Inter, weights 300–700) via `@import`
- [ ] Global reset: `box-sizing: border-box`, zero margins, `background: var(--bg-primary)`, `font-family: var(--font)`
- [ ] Define `@keyframes`: `fadeInUp`, `shimmer`, `glowPulse`, `float`
- [ ] Custom scrollbar styles matching the dark theme

#### 4.2 API Layer

- [ ] Create `src/api/client.js` — a `fetch`-based wrapper with typed error handling:
  - HTTP 200 → `{ success: true, recommendations, metadata }`
  - HTTP 404 → `{ success: false, errorType: "not_found", message: "..." }`
  - HTTP 422 → `{ success: false, errorType: "validation", message: "..." }`
  - `fetch` throws → `{ success: false, errorType: "connection", message: "..." }`

- [ ] Create `src/hooks/useRecommendations.js` — custom React hook managing:
  - `results` (array or null), `metadata` (object or null)
  - `isLoading` (boolean), `error` (object or null)
  - `search(formData)` — async callback that calls the API client
  - `clearResults()` — resets all state

#### 4.3 Components — Static / Layout

All icons from `react-icons/io5` (Ionicons 5).

- [ ] **`Hero`** — No props. Gradient-text heading with `IoRestaurant` icon, subtitle, animated gradient underline, tagline. Enters with `fadeInUp`.

- [ ] **`EmptyState`** — No props. Large floating `IoRestaurant` icon with `float` animation, heading, subtext, and a tip using `IoInformationCircle`.

- [ ] **`ErrorBanner`** — Props: `type` (`"error"` | `"warning"`), `message`, `onDismiss`. Uses `IoAlertCircle` (red) or `IoWarning` (gold), message text, `IoClose` dismiss button. Enters with `fadeInUp`.

- [ ] **`ResultsHeader`** — Props: `count`. Renders `"✨ Top {count} Picks For You"` with `IoSparkles` icon and animated gradient underline.

- [ ] **`StatsBar`** — Props: `metadata`. Horizontal flex row of pill-shaped chips, each with a `react-icons` icon:
  - `IoLocationSharp` + location (blue)
  - `IoWallet` + budget (green)
  - `IoPizza` + cuisine (accent)
  - `IoStar` + min rating (gold)
  - `IoSearch` + candidates found (muted)

#### 4.4 Components — Interactive

- [ ] **`SearchForm`** — Props: `onSearch(formData)`, `isLoading`. Glassmorphism card with 2-column responsive grid (collapses to 1 column on `<768px`):
  - Row 1: `IoLocationSharp` Location (text input, required) + `IoWallet` Budget (select dropdown)
  - Row 2: `IoPizza` Cuisine (text input, optional) + `IoStar` Min Rating (range input 0–5, step 0.5)
  - Row 3: `IoSparkles` Additional Preferences (textarea, full width)
  - Row 4: `IoOptions` Number of results (number input 1–10) + `IoSearch` Submit button (gradient CTA, disabled while loading)
  - Inline validation: shows `IoAlertCircle` error if location is empty on submit
  - All inputs controlled via `useState`

- [ ] **`RecommendationCard`** — Props: `recommendation`, `index`. Glassmorphism card with:
  - **Rank badge:** `IoTrophy` icon with gold/silver/bronze gradient for ranks 1–3; numeral badge for 4+
  - **Star rating:** `IoStar` (filled, gold) and `IoStarOutline` (empty, muted)
  - **Metadata chips:** `IoPizza` cuisine, `IoStar` rating, `IoWallet` cost — each in a pill with category-colored border
  - **AI Insight section:** `IoSparkles` icon header + explanation text on a slightly darker background
  - **Animation:** `fadeInUp` with `animation-delay: index * 0.12s` for staggered entrance; `glowPulse` border on hover

- [ ] **`SkeletonCard`** — Props: `count` (default 3). Pulsing shimmer placeholder cards mimicking `RecommendationCard` shape. Uses `shimmer` keyframe animation.

#### 4.5 App Assembly (`App.jsx`)

- [ ] Wire all components with `useRecommendations` hook
- [ ] Conditional rendering flow: Empty state → Loading skeleton → Error banner / Results
- [ ] Full data flow: form submit → skeleton cards appear → API call → cards render with staggered animation

```jsx
function App() {
    const { results, metadata, isLoading, error, search, clearResults } =
        useRecommendations();
    const hasSearched = results !== null || error !== null;

    return (
        <div className="app">
            <Hero />
            <main className="main-content">
                <SearchForm onSearch={search} isLoading={isLoading} />
                {error && <ErrorBanner type={...} message={...} onDismiss={clearResults} />}
                {isLoading && <SkeletonCard count={3} />}
                {results?.length > 0 && (
                    <section className="results-section">
                        <ResultsHeader count={results.length} />
                        {metadata && <StatsBar metadata={metadata} />}
                        {results.map((rec, i) => (
                            <RecommendationCard key={rec.rank} recommendation={rec} index={i} />
                        ))}
                    </section>
                )}
                {!hasSearched && !isLoading && <EmptyState />}
            </main>
        </div>
    );
}
```

#### 4.6 Backend CORS Update

- [ ] Add `CORSMiddleware` to `src/main.py` to allow cross-origin requests from the React dev server:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> **Note:** The Vite proxy handles routing in dev, but CORS is still needed for production or direct browser access.

#### 4.7 Documentation Update

- [ ] Update `README.md` with dual-terminal startup instructions:

```bash
# Terminal 1 — Start the FastAPI backend
cd SmartDine
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8000

# Terminal 2 — Start the React frontend
cd SmartDine/frontend
npm run dev
# Opens at http://localhost:5173
```

---

### Dependencies

> Phase 3 must be complete. `POST /api/v1/recommend` must return real AI-generated recommendations.
> Node.js (v18+) and npm must be installed.

---

### Acceptance Criteria

- [ ] `npm run build` inside `frontend/` completes with zero errors
- [ ] Opening `http://localhost:5173` shows the dark-themed SmartDine UI with Hero section, Inter font, and empty state
- [ ] Search form is centered, 2-column layout on desktop, 1-column on mobile (<768px)
- [ ] Submitting a valid form (e.g., location=`"Koramangala"`, budget=`"medium"`) shows skeleton loading cards → then glassmorphism recommendation cards within 5 seconds
- [ ] Cards appear with staggered `fadeInUp` animation and show subtle glow on hover
- [ ] Each card displays: `IoTrophy` rank badge, `IoStar`/`IoStarOutline` star rating, cuisine/cost chips with `react-icons`, and an `IoSparkles` AI Insight section
- [ ] Stats bar shows metadata as styled pill chips with `react-icons`
- [ ] Submitting an unknown location shows a styled gold warning banner (not a raw error)
- [ ] If FastAPI is not running, the UI shows a styled red error banner with a connection message
- [ ] Error banners can be dismissed with an `IoClose` × button
- [ ] The UI is usable on a standard 1080p screen without horizontal scrolling
- [ ] Browser tab shows `"SmartDine — AI Restaurant Recommendations"`

---

## Phase 5 — Hardening

### Objective

Harden the MVP for reliability, observability, and maintainability. Add LLM response caching to reduce repeat-query latency, comprehensive error handling for all failure modes, a complete test suite, and polished documentation. After this phase, SmartDine is ready for a demo or initial deployment.

---

### Key Tasks

#### 5.1 In-Memory Response Caching

- [ ] Implement a TTL cache in `src/core/filter_engine.py` or a new `src/core/cache.py` using `cachetools`:

```python
# src/core/cache.py
from cachetools import TTLCache
import hashlib, json

# Cache up to 256 unique queries; expire after 10 minutes
_cache: TTLCache = TTLCache(maxsize=256, ttl=600)

def make_cache_key(req_dict: dict) -> str:
    """Generate a deterministic cache key from the request body."""
    canonical = json.dumps(req_dict, sort_keys=True)
    return hashlib.md5(canonical.encode()).hexdigest()

def get_cached(key: str):
    return _cache.get(key)

def set_cached(key: str, value):
    _cache[key] = value
```

- [ ] In `src/api/routes.py`, before calling the filter engine:
  - Compute `cache_key = make_cache_key(body.model_dump())`
  - If `get_cached(cache_key)` is not `None`, return the cached response immediately with `X-Cache: HIT` response header
  - After a successful LLM call, call `set_cached(cache_key, response)`
  - Add `X-Cache: MISS` header on fresh responses

#### 5.2 Error Handling Audit

- [ ] **Dataset load failure:** Wrap `load_and_clean()` in a try/except. If it fails, log a critical error and raise `RuntimeError` to abort server startup (fast-fail is better than a partially-working server)
- [ ] **Filter engine returns empty DataFrame:** Handled by the `404` in `routes.py` — verify this is tested
- [ ] **Groq API `RateLimitError`:** `tenacity` already retries — additionally catch `groq.RateLimitError` specifically and return `503 Service Unavailable` with `Retry-After: 60` header
- [ ] **Groq API `AuthenticationError`:** Catch at startup, log a clear message: `"GROQ_API_KEY is invalid. Get a free key at console.groq.com"`, abort startup
- [ ] **LLM JSON parse failure:** Parser raises `ValueError` — fallback in `routes.py` returns raw filtered candidates (implemented in Phase 3)
- [ ] **Streamlit → FastAPI connection refused:** Handled in Phase 4 `st.error` block — verify with a test

#### 5.3 Structured Logging

- [ ] Configure `logging.basicConfig` in `src/main.py` with format: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
- [ ] Add request/response logging middleware to FastAPI:

```python
# src/main.py
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response
```

#### 5.4 Complete Test Suite

- [ ] Ensure test coverage for all modules:

| Test File | Tests |
|---|---|
| `tests/test_ingestion.py` | 6 tests (Phase 1) |
| `tests/test_filter_engine.py` | 8 tests (Phase 2) |
| `tests/test_prompt_builder.py` | 4 tests (Phase 3) |
| `tests/test_api.py` | 6 integration tests (Phase 2 + Phase 3) |

- [ ] Add the following new tests in Phase 5:
  - `test_cache_hit_returns_same_response()` — call `/recommend` twice with the same body; assert second call has `X-Cache: HIT`
  - `test_cache_miss_on_different_request()` — different `location` values produce different cache keys
  - `test_health_endpoint_returns_ok()` — `GET /health` returns `{"status": "ok"}`
  - `test_rate_limit_returns_503()` — mock Groq `RateLimitError`, assert API returns `503`

- [ ] Run the complete suite: `pytest tests/ -v --tb=short`
- [ ] Aim for **≥ 80% line coverage**: `pytest tests/ --cov=src --cov-report=term-missing`

#### 5.5 Final Documentation

- [ ] Update `README.md` with complete sections:
  - **Project Overview** — what SmartDine does
  - **Tech Stack** — table of all technologies
  - **Prerequisites** — Python 3.10+, `GROQ_API_KEY`
  - **Installation** — step-by-step `clone → venv → pip install → .env`
  - **Running the App** — dual-terminal instructions
  - **API Reference** — `POST /api/v1/recommend` request/response schema, `GET /health`
  - **Project Structure** — the folder tree
  - **Limitations & Roadmap** — point to `architecture.md` Section 6

- [ ] Add docstrings to all public functions in `src/` if not already present
- [ ] Verify `.env.example` has all variables with clear comments

#### 5.6 Pre-Commit Checklist

- [ ] Run `pip freeze > requirements.txt` to pin exact versions for reproducibility
- [ ] Ensure `.env` is **not** staged: `git status` should not show `.env`
- [ ] Run full test suite one final time: `pytest tests/ -v`
- [ ] Verify Streamlit UI end-to-end manually with at least 3 different queries
- [ ] Stage all changes: `git add .`
- [ ] Commit: `feat: complete MVP implementation of SmartDine AI recommendation system`

---

### Dependencies

> All previous phases (0–4) must be complete and their acceptance criteria met.

---

### Acceptance Criteria

- [ ] `pytest tests/ -v` — **all tests pass** with **zero failures**
- [ ] Code coverage ≥ 80%: `pytest tests/ --cov=src --cov-report=term-missing`
- [ ] Second identical request to `/recommend` returns `X-Cache: HIT` header and responds in **< 50ms** (cache hit)
- [ ] If `GROQ_API_KEY` is set to an invalid value, the server **fails to start** with a clear error message — it does NOT silently return errors at request time
- [ ] `README.md` contains working installation and run instructions verified on a clean environment
- [ ] No `.env` file is committed to Git

---

## Quick Reference: File × Phase Mapping

| File | Created In | Purpose |
|---|---|---|
| `src/config.py` | Phase 0 | Centralised settings via `pydantic-settings` |
| `.env.example` | Phase 0 | Template for environment variables |
| `src/data/ingestion.py` | Phase 1 | Load & clean HF dataset |
| `src/main.py` | Phase 1 | FastAPI app with `lifespan` dataset loader |
| `src/api/schemas.py` | Phase 2 | Pydantic request/response models |
| `src/core/filter_engine.py` | Phase 2 | Cascaded Pandas filter + progressive fallback |
| `src/api/routes.py` | Phase 2 → Phase 3 | `/recommend` endpoint (stubbed → LLM-wired) |
| `src/core/prompt_builder.py` | Phase 3 | System + user prompt templates |
| `src/core/llm_client.py` | Phase 3 | Async Groq API client with retry |
| `src/core/parser.py` | Phase 3 | LLM JSON → Pydantic model |
| `frontend/` | Phase 4 | Vite + React SPA (components, hooks, API client, CSS) |
| `src/core/cache.py` | Phase 5 | TTL cache for LLM responses |
| `tests/*.py` | Phase 1–5 | Unit + integration tests |
| `README.md` | Phase 0 → Phase 5 | Documentation (built up incrementally) |

---

## Technology Stack Summary

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

> **All technologies are 100% free.** No credit card, no paid tier, no self-hosted infrastructure required.

---

> **See also:**
> - [`context.md`](./context.md) — Problem statement and workflow
> - [`architecture.md`](./architecture.md) — Full technical architecture, data flow, and scalability roadmap
