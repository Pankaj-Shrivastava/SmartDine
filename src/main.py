import os
import asyncio
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.data.ingestion import load_and_clean
from src.config import get_settings
from src.api.routes import router

settings = get_settings()
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


async def _load_dataset_background(app: FastAPI) -> None:
    """Load and clean the dataset in a thread pool so the server port opens immediately."""
    logger.info("SmartDine API starting — loading dataset in background...")
    try:
        # Run the blocking I/O + CPU work off the event loop thread
        df = await asyncio.to_thread(load_and_clean)
        app.state.df = df
        app.state.loading = False
        logger.info(f"Dataset ready: {len(df)} restaurants in memory")
    except Exception as e:
        logger.critical(f"Dataset load failure: {e}", exc_info=True)
        app.state.loading = False
        app.state.loading_error = str(e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Mark as loading — the port binds immediately so Railway health checks pass
    app.state.df = None
    app.state.loading = True
    app.state.loading_error = None

    # Kick off dataset loading without blocking startup
    asyncio.create_task(_load_dataset_background(app))

    yield
    logger.info("SmartDine API shutting down")


app = FastAPI(
    title="SmartDine API",
    description="AI-Powered Restaurant Recommendation System",
    version="1.0.0",
    lifespan=lifespan,
)

# Build CORS origins — always allow local dev; add production Vercel URL via env var
_cors_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
_frontend_url = os.getenv("FRONTEND_URL", "").strip()
if _frontend_url:
    _cors_origins.append(_frontend_url)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000, 2)
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration}ms)")
    return response


app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """
    Always returns HTTP 200 so Railway's health check never triggers a restart.
    The 'status' field communicates the actual state to clients:
    - 'loading': dataset is still being fetched in background
    - 'ok': dataset is ready
    - 'error': dataset load failed (server is up but recommendations unavailable)
    """
    if getattr(app.state, "loading", True):
        return {"status": "loading", "restaurants_loaded": 0}

    if getattr(app.state, "loading_error", None):
        return {"status": "error", "detail": app.state.loading_error, "restaurants_loaded": 0}

    try:
        loaded = len(app.state.df)
    except (AttributeError, TypeError):
        loaded = 0

    return {"status": "ok", "restaurants_loaded": loaded}
