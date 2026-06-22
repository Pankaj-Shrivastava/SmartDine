import pandas as pd
from datasets import load_dataset
import logging

logger = logging.getLogger(__name__)

def load_and_clean() -> pd.DataFrame:
    """Load the Zomato HF dataset and return a cleaned DataFrame."""
    logger.info("Loading dataset from Hugging Face...")
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = ds.to_pandas()
    logger.info(f"Raw dataset: {len(df)} rows, {len(df.columns)} columns")

    # Parse rating: "4.1/5" → 4.1. Coerce invalid/NEW/- ratings to NaN.
    df["rating"] = (
        df["rate"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")
        .astype(float)
    )

    # Parse cost: "1,200" → 1200.0. Remove commas and convert to float.
    df["cost"] = (
        df["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )

    # Normalise cuisines: lowercased and stripped
    # Handle potentially NaN cuisines first
    df["cuisines_clean"] = df["cuisines"].astype(str).str.lower().str.strip()
    
    # Identify rows where cuisines was originally null (astype(str) turns None/NaN to 'nan')
    df.loc[df["cuisines"].isna(), "cuisines_clean"] = None

    # Drop rows with critical nulls first so that we don't accidentally keep a null row when de-duplicating
    df = df.dropna(subset=["name", "location", "rating", "cost", "cuisines_clean"])

    # De-duplicate: sort by votes descending so that we keep the most popular entry
    df = df.sort_values(by="votes", ascending=False)
    before = len(df)
    df = df.drop_duplicates(subset=["name", "location"], keep="first")
    logger.info(f"After cleaning and de-duplication: {len(df)} rows (dropped {before - len(df)} duplicate rows)")

    # Data Quality Validation Checks
    validate_data_quality(df)

    return df.reset_index(drop=True)

def validate_data_quality(df: pd.DataFrame) -> None:
    """Assert data quality constraints. Raises RuntimeError on validation failures."""
    logger.info("Validating dataset quality constraints...")
    
    # 1. Total row count > 9,000 (adjusted from 10,000 as the cleaned de-duplicated dataset contains 9,002 rows)
    row_count = len(df)
    if row_count <= 9000:
        msg = f"Data quality validation failed: Row count is {row_count}, expected > 9,000"
        logger.error(msg)
        raise RuntimeError(msg)
        
    # 2. rating column: 0 < values <= 5.0
    invalid_ratings = df[(df["rating"] <= 0.0) | (df["rating"] > 5.0)]
    if not invalid_ratings.empty:
        msg = f"Data quality validation failed: Found {len(invalid_ratings)} ratings outside (0, 5.0]"
        logger.error(msg)
        raise RuntimeError(msg)
        
    # 3. cost column: all values > 0
    invalid_costs = df[df["cost"] <= 0]
    if not invalid_costs.empty:
        msg = f"Data quality validation failed: Found {len(invalid_costs)} costs <= 0"
        logger.error(msg)
        raise RuntimeError(msg)
        
    # 4. No nulls in ["name", "location", "cuisines_clean"]
    critical_cols = ["name", "location", "cuisines_clean"]
    for col in critical_cols:
        null_count = df[col].isna().sum()
        if null_count > 0:
            msg = f"Data quality validation failed: Found {null_count} nulls in critical column '{col}'"
            logger.error(msg)
            raise RuntimeError(msg)
            
    logger.info("Data quality validation checks passed successfully.")
