import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Pre-built parquet bundled in the repo — zero network, instant load, ~208 KB.
# Regenerate with:  python scripts/build_dataset.py
_PARQUET_PATH = os.path.join(os.path.dirname(__file__), "zomato_clean.parquet")

# Fallback: HuggingFace CSV (used only if parquet is absent — e.g. local dev without it)
_REQUIRED_COLUMNS = [
    "name", "location", "cuisines",
    "rate", "approx_cost(for two people)", "votes",
]
_HF_CSV_URL = (
    "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
    "/resolve/main/zomato.csv"
)


def load_and_clean() -> pd.DataFrame:
    """
    Load the cleaned Zomato dataset.

    Primary path  → reads pre-built parquet from disk (instant, no network).
    Fallback path → downloads raw CSV from HuggingFace and cleans on the fly.
    """
    if os.path.exists(_PARQUET_PATH):
        return _load_from_parquet()
    else:
        logger.warning(
            f"Parquet file not found at {_PARQUET_PATH}. "
            "Falling back to live HuggingFace CSV download. "
            "Run `python scripts/build_dataset.py` to generate the parquet."
        )
        return _load_from_csv()


# ---------------------------------------------------------------------------
# Primary path
# ---------------------------------------------------------------------------

def _load_from_parquet() -> pd.DataFrame:
    """Load the pre-built, pre-cleaned parquet file."""
    logger.info(f"Loading dataset from bundled parquet: {_PARQUET_PATH}")
    df = pd.read_parquet(_PARQUET_PATH)
    raw_count = len(df)
    logger.info(f"Loaded {raw_count} restaurants from parquet")
    validate_data_quality(df, raw_count)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Fallback path (local dev / CI without parquet)
# ---------------------------------------------------------------------------

def _load_from_csv() -> pd.DataFrame:
    """Download and clean the raw CSV from HuggingFace."""
    logger.info("Downloading raw CSV from HuggingFace (fallback path)...")
    df = pd.read_csv(_HF_CSV_URL, usecols=_REQUIRED_COLUMNS, low_memory=False)
    raw_count = len(df)
    logger.info(f"Raw dataset: {raw_count} rows")

    # Rating: "4.1/5" → 4.1; "NEW"/"-" → NaN; 0.0 and >5.0 → NaN
    df["rating"] = (
        df["rate"].astype(str).str.extract(r"(\d+\.?\d*)").astype(float)
    )
    df.loc[df["rating"] <= 0.0, "rating"] = pd.NA
    df.loc[df["rating"] > 5.0, "rating"] = pd.NA

    # Cost: "1,200" → 1200; non-numeric / ≤0 → NaN
    df["cost"] = (
        df["approx_cost(for two people)"]
        .astype(str).str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
    df.loc[df["cost"] <= 0, "cost"] = pd.NA

    # Cuisines
    df["cuisines_clean"] = df["cuisines"].astype(str).str.lower().str.strip()
    df.loc[df["cuisines"].isna() | (df["cuisines_clean"] == "nan"), "cuisines_clean"] = pd.NA

    before_drop = len(df)
    df = df.dropna(subset=["name", "location", "rating", "cost", "cuisines_clean"])
    logger.info(f"Dropped {before_drop - len(df)} invalid rows; {len(df)} remain")

    df = df.sort_values("votes", ascending=False)
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["name", "location"], keep="first")
    logger.info(f"After dedup: {len(df)} rows (dropped {before_dedup - len(df)} duplicates)")

    validate_data_quality(df, raw_count)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Shared validation (warnings only — never crashes the server)
# ---------------------------------------------------------------------------

def validate_data_quality(df: pd.DataFrame, raw_count: int) -> None:
    """Log data quality warnings. Does NOT raise."""
    logger.info("Validating dataset quality...")
    passed = True

    row_count = len(df)
    min_expected = max(100, int(raw_count * 0.10))
    if row_count < min_expected:
        logger.warning(
            f"Quality warning: {row_count} rows (expected >= {min_expected}). "
            "Recommendation quality may be degraded."
        )
        passed = False
    else:
        logger.info(f"Row count OK: {row_count} rows")

    rating_col = "rating" if "rating" in df.columns else None
    if rating_col:
        bad = df[(df[rating_col] <= 0) | (df[rating_col] > 5.0)]
        if not bad.empty:
            logger.warning(f"Quality warning: {len(bad)} rows with rating outside (0, 5.0]")
            passed = False

    cost_col = "cost" if "cost" in df.columns else None
    if cost_col:
        bad = df[df[cost_col] <= 0]
        if not bad.empty:
            logger.warning(f"Quality warning: {len(bad)} rows with cost <= 0")
            passed = False

    for col in ["name", "location", "cuisines_clean"]:
        if col in df.columns:
            n = df[col].isna().sum()
            if n > 0:
                logger.warning(f"Quality warning: {n} nulls in '{col}'")
                passed = False

    if passed:
        logger.info("All quality checks passed.")
    else:
        logger.warning("Quality warnings present — server continues with available data.")
