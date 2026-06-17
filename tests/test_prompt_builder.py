import pytest
import pandas as pd
from src.core.prompt_builder import build_system_prompt, build_user_prompt
from src.api.schemas import RecommendationRequest

@pytest.fixture
def sample_candidates():
    """Create a sample pandas DataFrame containing restaurant candidates."""
    return pd.DataFrame([
        {
            "name": "Restaurant A",
            "location": "Koramangala",
            "cuisines": "Italian, Pizza",
            "rating": 4.5,
            "cost": 500.0,
            "rest_type": "Casual Dining",
            "book_table": "Yes",
            "dish_liked": "Pasta, Pizza",
            "votes": 120
        },
        {
            "name": "Restaurant B",
            "location": "Koramangala",
            "cuisines": "Italian, Pasta",
            "rating": 4.2,
            "cost": 400.0,
            "rest_type": "Cafe",
            "book_table": "No",
            "dish_liked": "Coffee, Lasagna",
            "votes": 80
        }
    ])

def test_system_prompt_contains_json_schema():
    """Verify that the system prompt defines and includes the correct JSON output schema."""
    prompt = build_system_prompt(top_n=5)
    assert "recommendations" in prompt
    assert "rank" in prompt
    assert "name" in prompt
    assert "cuisine" in prompt
    assert "rating" in prompt
    assert "cost_for_two" in prompt
    assert "explanation" in prompt

def test_user_prompt_contains_location(sample_candidates):
    """Verify that the user prompt contains the specified location."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        top_n=3
    )
    prompt = build_user_prompt(req, sample_candidates, 301, 800)
    assert "Koramangala" in prompt

def test_user_prompt_markdown_table(sample_candidates):
    """Verify that the candidate restaurants list is converted to a Markdown table in the user prompt."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        top_n=3
    )
    prompt = build_user_prompt(req, sample_candidates, 301, 800)
    # Markdown tables contain vertical pipes '|' for cell division
    assert "|" in prompt
    assert "Name" in prompt
    assert "Cost (₹ for 2)" in prompt
    assert "Restaurant A" in prompt
    assert "Restaurant B" in prompt

def test_user_prompt_cuisine_any_when_none(sample_candidates):
    """Verify that if no cuisine is specified in the request, the user prompt falls back to 'Any'."""
    req = RecommendationRequest(
        location="Koramangala",
        budget="medium",
        cuisine=None,
        min_rating=4.0,
        top_n=3
    )
    prompt = build_user_prompt(req, sample_candidates, 301, 800)
    assert "Cuisine: Any" in prompt
