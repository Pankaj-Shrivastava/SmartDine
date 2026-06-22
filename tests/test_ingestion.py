# pyrefly: ignore [missing-import]
import pytest
import pandas as pd
from src.data.ingestion import load_and_clean

@pytest.fixture(scope="module")
def cleaned_df():
    """Fixture to load and clean the dataset once for the test module."""
    return load_and_clean()

def test_dataframe_not_empty(cleaned_df):
    """Verify the dataset has a significant number of clean rows.
    The pre-built parquet contains 9,216 restaurants after cleaning + dedup.
    """
    assert cleaned_df is not None
    assert len(cleaned_df) >= 5_000, (
        f"Expected >= 5,000 rows, got {len(cleaned_df)}"
    )

def test_rating_column_type(cleaned_df):
    """Verify that the rating column is numeric (float)."""
    assert pd.api.types.is_float_dtype(cleaned_df["rating"])

def test_cost_column_type(cleaned_df):
    """Verify that the cost column is numeric (float)."""
    assert pd.api.types.is_float_dtype(cleaned_df["cost"])

def test_no_critical_nulls(cleaned_df):
    """Verify that there are no null values in critical columns."""
    critical_cols = ["name", "location", "rating", "cost", "cuisines_clean"]
    for col in critical_cols:
        null_count = cleaned_df[col].isna().sum()
        assert null_count == 0, f"Found {null_count} nulls in critical column '{col}'"

def test_rating_range(cleaned_df):
    """Verify that all rating values lie strictly within the range (0.0, 5.0]."""
    assert (cleaned_df["rating"] > 0.0).all()
    assert (cleaned_df["rating"] <= 5.0).all()

def test_cuisines_normalised(cleaned_df):
    """Verify that cuisines are clean, lowercase, and stripped of extra whitespaces."""
    # Ensure they are lowercase
    assert cleaned_df["cuisines_clean"].str.lower().equals(cleaned_df["cuisines_clean"])
    # Ensure they don't have leading/trailing whitespaces
    assert cleaned_df["cuisines_clean"].str.strip().equals(cleaned_df["cuisines_clean"])
