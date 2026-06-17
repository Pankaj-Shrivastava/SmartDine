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
    """Filter restaurants according to user preferences and return the top matches (stubbed LLM)."""
    try:
        df = request.app.state.df
    except AttributeError as e:
        logger.critical("FastAPI app state is missing the dataset DataFrame.", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error: Dataset is not loaded in memory."
        ) from e

    candidates = filter_restaurants(df, body)

    if candidates.empty:
        raise HTTPException(
            status_code=404,
            detail="No restaurants found matching your criteria. Try broadening your filters."
        )

    # Convert the top_n candidate rows into Recommendation schemas
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
