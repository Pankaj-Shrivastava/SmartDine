import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Only the columns our application actually uses — loading all 17 columns wastes ~65% RAM
_REQUIRED_COLUMNS = [
    "name",
    "location",
    "cuisines",
    "rate",
    "approx_cost(for two people)",
    "votes",
]

# HuggingFace raw CSV URL — bypasses the `datasets` library (Arrow buffer overhead)
# and loads directly into pandas, cutting peak memory usage by ~60-70%.
_HF_CSV_URL = (
    "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
    "/resolve/main/zomato.csv"
)


def load_and_clean() -> pd.DataFrame:
    """
    Load the Zomato dataset and return a cleaned DataFrame.

    Loads the raw CSV directly from HuggingFace (bypassing the `datasets` Arrow
    pipeline) to stay well within Railway's 512 MB memory limit.
    """
    logger.info("Loading dataset from HuggingFace CSV (memory-efficient path)...")
    try:
        df = pd.read_csv(
            _HF_CSV_URL,
            usecols=_REQUIRED_COLUMNS,
            low_memory=False,
        )
        logger.info(f"Raw dataset: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        logger.error(f"CSV load failed ({e}); falling back to datasets library...")
        df = _load_via_datasets_library()

    raw_count = len(df)

    # --- Rating parsing ---
    # Extract first numeric part from strings like "4.1/5", "NEW", "-"
    df["rating"] = (
        df["rate"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")
        .astype(float)
    )
    # 0.0 = sentinel "no rating"; > 5.0 = erroneous — discard both
    df.loc[df["rating"] <= 0.0, "rating"] = pd.NA
    df.loc[df["rating"] > 5.0, "rating"] = pd.NA

    # --- Cost parsing ---
    # "1,200" → 1200.0; non-numeric → NaN; zero/negative → NaN
    df["cost"] = (
        df["approx_cost(for two people)"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
    df.loc[df["cost"] <= 0, "cost"] = pd.NA

    # --- Cuisine normalisation ---
    df["cuisines_clean"] = df["cuisines"].astype(str).str.lower().str.strip()
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


def _load_via_datasets_library() -> pd.DataFrame:
    """Fallback: load via HuggingFace datasets library if direct CSV download fails."""
    from datasets import load_dataset  # deferred import — not needed on the happy path
    logger.info("Loading via datasets library (fallback)...")
    ds = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = ds.to_pandas()
    # Keep only the required columns to limit memory
    available = [c for c in _REQUIRED_COLUMNS if c in df.columns]
    return df[available]


def validate_data_quality(df: pd.DataFrame, raw_count: int) -> None:
    """
    Run data quality checks and log warnings for any failures.
    Does NOT raise — the server starts with whatever clean data is available.
    """
    logger.info("Validating dataset quality constraints...")
    passed = True

    # 1. Cleaned row count must be >= 10% of raw count
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

    # 2. No remaining ratings outside (0, 5.0]
    invalid_ratings = df[(df["rating"] <= 0.0) | (df["rating"] > 5.0)]
    if not invalid_ratings.empty:
        logger.warning(
            f"Data quality warning: {len(invalid_ratings)} rows have ratings outside (0, 5.0]. "
            f"Sample: {invalid_ratings['rating'].head(5).tolist()}"
        )
        passed = False

    # 3. No remaining costs <= 0
    invalid_costs = df[df["cost"] <= 0]
    if not invalid_costs.empty:
        logger.warning(
            f"Data quality warning: {len(invalid_costs)} rows have cost <= 0. "
            f"Sample: {invalid_costs['cost'].head(5).tolist()}"
        )
        passed = False

    # 4. No nulls in critical string columns
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
