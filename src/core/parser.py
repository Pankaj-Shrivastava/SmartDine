import logging
from typing import Any
from src.api.schemas import Recommendation, RecommendationResponse, QueryMetadata
from pydantic import ValidationError

logger = logging.getLogger(__name__)

def parse_llm_response(
    raw: dict[str, Any],
    query_metadata: QueryMetadata,
) -> RecommendationResponse:
    """Validate LLM JSON response against the RecommendationResponse schema. Raises ValueError on failure."""
    try:
        if "recommendations" not in raw:
            raise KeyError("Missing 'recommendations' key in raw LLM response.")
            
        recs = [Recommendation(**r) for r in raw["recommendations"]]
        return RecommendationResponse(
            recommendations=recs,
            query_metadata=query_metadata,
        )
    except (KeyError, ValidationError, TypeError) as e:
        logger.error(f"LLM response parsing failed: {e}")
        raise ValueError(f"Malformed LLM response: {e}") from e
