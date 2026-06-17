from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class RecommendationRequest(BaseModel):
    location: str = Field(
        ...,
        min_length=2,
        json_schema_extra={"example": "Koramangala"},
        description="Neighbourhood or city area name"
    )
    budget: Literal["low", "medium", "high"] = Field(
        ...,
        description="low (≤₹300) | medium (₹301–₹800) | high (₹801+)"
    )
    cuisine: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Italian"},
        description="Preferred cuisine type (optional)"
    )
    min_rating: float = Field(
        3.5,
        ge=0.0,
        le=5.0,
        description="Minimum acceptable rating (0.0–5.0)"
    )
    extras: Optional[str] = Field(
        None,
        json_schema_extra={"example": "family-friendly, table booking"},
        description="Free-text additional preferences"
    )
    top_n: int = Field(
        5,
        ge=1,
        le=10,
        description="Number of recommendations to return (1–10)"
    )

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
