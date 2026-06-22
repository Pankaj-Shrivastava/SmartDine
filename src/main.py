import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SmartDine API starting — loading dataset...")
    try:
        app.state.df = load_and_clean()
        logger.info(f"Dataset ready: {len(app.state.df)} restaurants in memory")
    except Exception as e:
        logger.critical(f"Dataset load failure: {e}", exc_info=True)
        # Aborting server startup as per Phase 5 / hardening recommendations:
        # "If it fails, log a critical error and raise RuntimeError to abort server startup"
        raise RuntimeError(f"Failed to load dataset on startup: {e}") from e
    yield
    logger.info("SmartDine API shutting down")

app = FastAPI(
    title="SmartDine API",
    description="AI-Powered Restaurant Recommendation System",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    # Return loading status
    try:
        loaded = len(app.state.df)
    except AttributeError:
        loaded = 0
    return {"status": "ok", "restaurants_loaded": loaded}
