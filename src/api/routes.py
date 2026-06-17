from fastapi import APIRouter, Request, HTTPException
from src.api.schemas import (
    RecommendationRequest, RecommendationResponse,
    Recommendation, QueryMetadata
)
from src.core.filter_engine import filter_restaurants, _get_budget_range
from src.core.prompt_builder import build_system_prompt, build_user_prompt
from src.core.llm_client import call_llm
from src.core.parser import parse_llm_response
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: Request, body: RecommendationRequest):
    """Filter restaurants according to user preferences and use LLM to generate recommendations with AI explanations. Falls back to stub explanations on failure."""
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

    # Calculate budget ranges for prompt context
    cost_low, cost_high = _get_budget_range(body.budget)
    cost_low_val = int(cost_low)
    cost_high_val = str(int(cost_high)) if cost_high != float("inf") else "Unlimited"

    # Construct the query metadata
    query_metadata = QueryMetadata(
        location=body.location,
        budget=body.budget,
        cuisine=body.cuisine,
        min_rating=body.min_rating,
        top_n=body.top_n,
        candidates_found=len(candidates),
    )

    # Build system and user prompts
    system_prompt = build_system_prompt(body.top_n)
    user_prompt = build_user_prompt(body, candidates, cost_low_val, cost_high_val)

    # Attempt to invoke the Groq LLM API and parse the response
    try:
        raw_response = await call_llm(system_prompt, user_prompt)
        return parse_llm_response(raw_response, query_metadata)
    except Exception as e:
        logger.warning(
            f"LLM recommendation or parsing failed. Falling back to structured default: {e}",
            exc_info=True
        )
        
        # Build fallback recommendations with AI unavailable explanations
        fallback_recs = [
            Recommendation(
                rank=i + 1,
                name=row["name"],
                cuisine=row["cuisines"],
                rating=round(float(row["rating"]), 1),
                cost_for_two=int(row["cost"]),
                explanation="AI service temporarily unavailable — showing top-rated matches.",
            )
            for i, (_, row) in enumerate(candidates.head(body.top_n).iterrows())
        ]
        
        return RecommendationResponse(
            recommendations=fallback_recs,
            query_metadata=query_metadata,
        )
