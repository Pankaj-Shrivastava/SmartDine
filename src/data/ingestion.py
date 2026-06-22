import pandas as pd
from datasets import load_dataset
import logging

logger = logging.getLogger(__name__)


def load_and_clean() -> pd.DataFrame:
    """Load the Zomato HF dataset and return a cleaned DataFrame."""
    logger.info("Loading dataset from Hugging Face...")
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = ds.to_pandas()
    raw_count = len(df)
    logger.info(f"Raw dataset: {raw_count} rows, {len(df.columns)} columns")

    # --- Rating parsing ---
    # Extract first numeric part from strings like "4.1/5", "NEW", "-"
    # Anything non-numeric (NEW, -, nan) becomes NaN via extract → astype(float)
    df["rating"] = (
        df["rate"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")
        .astype(float)
    )
    # Ratings of 0.0 are sentinel "no rating" values — treat as invalid
    df.loc[df["rating"] <= 0.0, "rating"] = pd.NA
    # Ratings above 5.0 are clearly erroneous — discard
    df.loc[df["rating"] > 5.0, "rating"] = pd.NA

    # --- Cost parsing ---
    # Remove commas ("1,200" → "1200") then coerce; non-numeric → NaN
    df["cost"] = (
        df["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
    # Zero or negative costs are invalid — discard
    df.loc[df["cost"] <= 0, "cost"] = pd.NA

    # --- Cuisine normalisation ---
    df["cuisines_clean"] = df["cuisines"].astype(str).str.lower().str.strip()
    # astype(str) converts None/NaN to the literal string "nan" — revert those to NaN
    df.loc[df["cuisines"].isna() | (df["cuisines_clean"] == "nan"), "cuisines_clean"] = pd.NA

    # --- Drop rows missing any critical field ---
    before_drop = len(df)
    df = df.dropna(subset=["name", "location", "rating", "cost", "cuisines_clean"])
    logger.info(
        f"Dropped {before_drop - len(df)} rows with missing/invalid fields; "
        f"{len(df)} remain"
    )

    # --- De-duplicate: keep the most-voted entry per (name, location) ---
    df = df.sort_values(by="votes", ascending=False)
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["name", "location"], keep="first")
    logger.info(
        f"After de-duplication: {len(df)} rows "
        f"(dropped {before_dedup - len(df)} duplicates)"
    )

    # --- Data quality checks (warnings only — server always starts) ---
    validate_data_quality(df, raw_count)

    return df.reset_index(drop=True)


def validate_data_quality(df: pd.DataFrame, raw_count: int) -> None:
    """
    Run data quality checks and log warnings for any failures.
    Does NOT raise — the server will start with whatever clean data is available
    rather than refusing to start entirely.
    """
    logger.info("Validating dataset quality constraints...")
    passed = True

    # 1. Cleaned row count should be at least 10% of the raw count
    row_count = len(df)
    min_expected = max(100, int(raw_count * 0.10))
    if row_count < min_expected:
        logger.warning(
            f"Data quality warning: Only {row_count} rows remain after cleaning "
            f"(expected >= {min_expected}, i.e. 10% of {raw_count} raw rows). "
            "Recommendation quality may be degraded."
        )
        passed = False
    else:
        logger.info(f"Row count check passed: {row_count} rows (>= {min_expected})")

    # 2. No remaining ratings outside (0, 5.0] — should have been cleared above
    invalid_ratings = df[(df["rating"] <= 0.0) | (df["rating"] > 5.0)]
    if not invalid_ratings.empty:
        logger.warning(
            f"Data quality warning: {len(invalid_ratings)} rows have ratings outside (0, 5.0] "
            "and slipped through cleaning. Sample values: "
            f"{invalid_ratings['rating'].head(5).tolist()}"
        )
        passed = False

    # 3. No remaining costs <= 0 — should have been cleared above
    invalid_costs = df[df["cost"] <= 0]
    if not invalid_costs.empty:
        logger.warning(
            f"Data quality warning: {len(invalid_costs)} rows have cost <= 0 "
            "and slipped through cleaning. Sample values: "
            f"{invalid_costs['cost'].head(5).tolist()}"
        )
        passed = False

    # 4. No nulls remaining in critical string columns
    for col in ["name", "location", "cuisines_clean"]:
        null_count = df[col].isna().sum()
        if null_count > 0:
            logger.warning(
                f"Data quality warning: {null_count} nulls remain in '{col}' after cleaning."
            )
            passed = False

    if passed:
        logger.info("All data quality checks passed.")
    else:
        logger.warning(
            "One or more data quality checks raised warnings. "
            "The server will continue with the available clean data."
        )
