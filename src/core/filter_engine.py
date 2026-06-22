import pandas as pd
import logging
from src.api.schemas import RecommendationRequest
from src.config import get_settings

logger = logging.getLogger(__name__)

def _get_budget_range(budget: str) -> tuple[float, float]:
    """Retrieve budget range based on settings thresholds."""
    settings = get_settings()
    return {
        "low":    (0.0, float(settings.budget_low_max)),
        "medium": (float(settings.budget_low_max + 1), float(settings.budget_medium_max)),
        "high":   (float(settings.budget_medium_max + 1), float("inf")),
    }[budget]

def filter_restaurants(df: pd.DataFrame, req: RecommendationRequest) -> pd.DataFrame:
    """Apply cascaded filters. Falls back progressively if results are empty."""
    max_candidates = get_settings().max_candidates

    # Level 0: Strict Location + Cuisine + Budget + Rating
    result = _apply_filters(df, req, use_cuisine=True, strict_location=True, use_budget=True, use_rating=True)

    # Fallback 1: Drop cuisine filter (if cuisine was specified)
    if result.empty and req.cuisine:
        logger.warning("No results with cuisine filter — relaxing cuisine constraint")
        result = _apply_filters(df, req, use_cuisine=False, strict_location=True, use_budget=True, use_rating=True)

    # Fallback 2: Drop cuisine + widen to city-level location
    if result.empty:
        logger.warning("No results for neighbourhood — widening to city-level location")
        result = _apply_filters(df, req, use_cuisine=False, strict_location=False, use_budget=True, use_rating=True)

    # Fallback 3: Return top-rated in location regardless of budget/cuisine/rating
    if result.empty:
        logger.warning("No results after all fallbacks — returning top-rated in location")
        result = _apply_filters(df, req, use_cuisine=False, strict_location=True, use_budget=False, use_rating=False)

    if result.empty:
        return pd.DataFrame()

    # Sort results: rating descending, then votes descending
    result = result.sort_values(by=["rating", "votes"], ascending=[False, False])
    return result.head(max_candidates)

def _apply_filters(
    df: pd.DataFrame,
    req: RecommendationRequest,
    use_cuisine: bool,
    strict_location: bool,
    use_budget: bool,
    use_rating: bool,
) -> pd.DataFrame:
    """Apply filters based on toggle flags."""
    res = df.copy()

    # 1. Location filter
    if strict_location:
        res = res[res["location"].str.lower().str.contains(req.location.lower(), na=False)]
    else:
        if "listed_in(city)" in res.columns:
            res = res[res["listed_in(city)"].str.lower().str.contains(req.location.lower(), na=False)]
        else:
            res = res[res["location"].str.lower().str.contains(req.location.lower(), na=False)]

    # 2. Budget filter
    if use_budget:
        low, high = _get_budget_range(req.budget)
        res = res[(res["cost"] >= low) & (res["cost"] <= high)]

    # 3. Cuisine filter (optional)
    if use_cuisine and req.cuisine:
        res = res[res["cuisines_clean"].str.contains(req.cuisine.lower(), na=False)]

    # 4. Rating filter
    if use_rating:
        res = res[res["rating"] >= req.min_rating]

    return res
