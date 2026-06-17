import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    """Initialise FastAPI test client. Lifespan event loads the dataset."""
    with TestClient(app) as c:
        yield c

def test_recommend_returns_200(client):
    """Verify that a valid request returns 200 OK."""
    payload = {
        "location": "Koramangala",
        "budget": "medium",
        "cuisine": "Italian",
        "min_rating": 3.0,
        "top_n": 5
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200

def test_recommend_schema_valid(client):
    """Verify that the response structure conforms to RecommendationResponse schema."""
    payload = {
        "location": "Koramangala",
        "budget": "medium",
        "min_rating": 3.0,
        "top_n": 2
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Assert fields in response
    assert "recommendations" in data
    assert "query_metadata" in data
    
    # Verify recommendations
    recs = data["recommendations"]
    assert len(recs) > 0
    for rec in recs:
        assert "rank" in rec
        assert "name" in rec
        assert "cuisine" in rec
        assert "rating" in rec
        assert "cost_for_two" in rec
        assert "explanation" in rec
        assert rec["explanation"] == "[AI explanation coming in Phase 3]"
        
    # Verify query_metadata
    meta = data["query_metadata"]
    assert meta["location"] == "Koramangala"
    assert meta["budget"] == "medium"
    assert meta["min_rating"] == 3.0
    assert meta["top_n"] == 2
    assert "candidates_found" in meta

def test_invalid_budget_returns_422(client):
    """Verify that invalid budget string returns 422 Unprocessable Entity."""
    payload = {
        "location": "Koramangala",
        "budget": "very cheap",  # Invalid literal
        "top_n": 5
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 422

def test_missing_location_returns_422(client):
    """Verify that missing required location parameter returns 422 Unprocessable Entity."""
    payload = {
        "budget": "medium",
        "top_n": 5
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 422

def test_top_n_respected(client):
    """Verify that the number of returned recommendations matches top_n."""
    payload = {
        "location": "Koramangala",
        "budget": "medium",
        "top_n": 3
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) == 3

def test_unknown_location_returns_404(client):
    """Verify that a non-existent location returns 404 Not Found."""
    payload = {
        "location": "ZZZNonExistentCity",
        "budget": "medium",
        "top_n": 5
    }
    response = client.post("/api/v1/recommend", json=payload)
    assert response.status_code == 404
    assert "detail" in response.json()
