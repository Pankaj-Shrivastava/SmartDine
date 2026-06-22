import pandas as pd
from src.api.schemas import RecommendationRequest

SYSTEM_PROMPT_TEMPLATE = """\
You are SmartDine, an expert restaurant recommendation engine.

You will receive:
1. A user's dining preferences.
2. A table of candidate restaurants (pre-filtered from a larger dataset).

Your task:
- Analyse each candidate against the user's preferences.
- Rank the top {top_n} restaurants.
- For each, provide a concise explanation of WHY it's a good fit.

Respond ONLY with a JSON object in this exact schema:
{{
  "recommendations": [
    {{
      "rank": 1,
      "name": "Restaurant Name",
      "cuisine": "Cuisine Type",
      "rating": 4.5,
      "cost_for_two": 600,
      "explanation": "One-paragraph explanation."
    }}
  ]
}}

Ranking criteria (in order of priority):
1. How well the cuisine matches the user's preference.
2. Rating (higher is better).
3. Cost alignment with stated budget.
4. Relevance of additional preferences (e.g., "family-friendly" → prefer Casual Dining or book_table=Yes).
5. Popularity (vote count).

Do NOT include restaurants that are clearly irrelevant.
Do NOT invent data — use only the provided table.
"""

USER_PROMPT_TEMPLATE = """\
## User Preferences
- Location: {location}
- Budget: {budget} (₹{cost_low}–₹{cost_high} for two)
- Cuisine: {cuisine}
- Minimum Rating: {min_rating}
- Additional Preferences: {extras}

## Candidate Restaurants
{markdown_table}

Please rank the top {top_n} restaurants and explain your reasoning.
"""

def build_system_prompt(top_n: int) -> str:
    """Construct the system instructions for the LLM recommendation engine."""
    return SYSTEM_PROMPT_TEMPLATE.format(top_n=top_n)

def build_user_prompt(
    req: RecommendationRequest,
    candidates: pd.DataFrame,
    cost_low: int,
    cost_high: int
) -> str:
    """Format user preferences and inject candidates as a Markdown table."""
    desired_columns = ["name", "location", "cuisines", "rating", "cost", "votes", "rest_type", "book_table", "dish_liked"]
    available_columns = [c for c in desired_columns if c in candidates.columns]

    markdown_table = candidates[available_columns].rename(columns={
        "name": "Name",
        "location": "Location",
        "cuisines": "Cuisines",
        "rating": "Rating",
        "cost": "Cost (₹ for 2)",
        "votes": "Votes",
        "rest_type": "Type",
        "book_table": "Book Table",
        "dish_liked": "Popular Dishes",
    }).to_markdown(index=False)

    return USER_PROMPT_TEMPLATE.format(
        location=req.location,
        budget=req.budget,
        cost_low=cost_low,
        cost_high=cost_high,
        cuisine=req.cuisine or "Any",
        min_rating=req.min_rating,
        extras=req.extras or "None specified",
        markdown_table=markdown_table,
        top_n=req.top_n,
    )
