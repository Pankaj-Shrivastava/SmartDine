import pytest
import pandas as pd
from src.data.ingestion import load_and_clean
from src.core.filter_engine import filter_restaurants
from src.api.schemas import RecommendationRequest
from src.config import get_settings

@pytest.fixture(scope="module")
def dataset():
    """Load and clean the dataset once for all filter engine tests."""
    return load_and_clean()

def test_location_filter(dataset):
    """Verify that location filtering returns only restaurants in the specified location."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        min_rating=3.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    # Every matched restaurant location should contain 'koramangala' case-insensitively
    for _, row in result.iterrows():
        assert "koramangala" in row["location"].lower()

def test_budget_filter_low(dataset):
    """Verify that budget='low' returns only restaurants with cost <= BUDGET_LOW_MAX."""
    settings = get_settings()
    req = RecommendationRequest(
        location="Koramangala",
        budget="low",
        min_rating=1.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    for _, row in result.iterrows():
        assert row["cost"] <= settings.budget_low_max

def test_budget_filter_medium(dataset):
    """Verify that budget='medium' returns restaurants within the medium budget range."""
    settings = get_settings()
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        min_rating=1.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    for _, row in result.iterrows():
        assert settings.budget_low_max < row["cost"] <= settings.budget_medium_max

def test_cuisine_filter(dataset):
    """Verify that cuisine filtering returns restaurants offering the requested cuisine."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        cuisine="Italian",
        min_rating=1.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    for _, row in result.iterrows():
        assert "italian" in row["cuisines_clean"]

def test_rating_filter(dataset):
    """Verify that min_rating constraint is strictly respected."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        min_rating=4.2,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    for _, row in result.iterrows():
        assert row["rating"] >= 4.2

def test_max_candidates_cap(dataset):
    """Verify that returned candidate list does not exceed MAX_CANDIDATES."""
    settings = get_settings()
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        min_rating=1.0,
        top_n=10
    )
    # The returned candidate list is capped at max_candidates (20) in the engine,
    # before being subsetted to top_n in the router.
    result = filter_restaurants(dataset, req)
    assert len(result) <= settings.max_candidates

def test_cuisine_fallback(dataset):
    """Verify that if a cuisine filter yields 0 matches, the engine falls back to drop cuisine filter."""
    # Request a non-existent cuisine in Koramangala
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        cuisine="NonExistentAlienCuisine",
        min_rating=3.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert not result.empty
    # Since it fell back to dropping the cuisine filter, cuisines will not match NonExistentAlienCuisine
    # but restaurants will still be returned from Koramangala
    for _, row in result.iterrows():
        assert "koramangala" in row["location"].lower()

def test_no_results_returns_empty_df(dataset):
    """Verify that query for non-existent location returns an empty DataFrame without errors."""
    req = RecommendationRequest(
        location="ZZZNonExistentCity",
        budget="medium",
        min_rating=1.0,
        top_n=5
    )
    result = filter_restaurants(dataset, req)
    assert result.empty
