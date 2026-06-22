"""
One-off script: downloads, cleans and saves the Zomato dataset as a compact
parquet file. Run once locally, commit the output file to the repo.

Usage (from project root, with venv active):
    python scripts/build_dataset.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
    "name",
    "location",
    "cuisines",
    "rate",
    "approx_cost(for two people)",
    "votes",
]

HF_CSV_URL = (
    "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation"
    "/resolve/main/zomato.csv"
)

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "src", "data", "zomato_clean.parquet")


def build():
    logger.info(f"Downloading CSV from HuggingFace...")
    df = pd.read_csv(HF_CSV_URL, usecols=REQUIRED_COLUMNS, low_memory=False)
    logger.info(f"Raw: {len(df)} rows")

    # Rating
    df["rating"] = df["rate"].astype(str).str.extract(r"(\d+\.?\d*)").astype(float)
    df.loc[df["rating"] <= 0.0, "rating"] = pd.NA
    df.loc[df["rating"] > 5.0, "rating"] = pd.NA

    # Cost
    df["cost"] = (
        df["approx_cost(for two people)"]
        .astype(str).str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
    df.loc[df["cost"] <= 0, "cost"] = pd.NA

    # Cuisines
    df["cuisines_clean"] = df["cuisines"].astype(str).str.lower().str.strip()
    df.loc[df["cuisines"].isna() | (df["cuisines_clean"] == "nan"), "cuisines_clean"] = pd.NA

    # Drop + dedup
    before = len(df)
    df = df.dropna(subset=["name", "location", "rating", "cost", "cuisines_clean"])
    logger.info(f"Dropped {before - len(df)} rows with missing fields; {len(df)} remain")
    df = df.sort_values("votes", ascending=False).drop_duplicates(["name", "location"], keep="first")
    logger.info(f"After dedup: {len(df)} rows")

    # Keep only what the app needs
    df = df[["name", "location", "cuisines", "cuisines_clean", "rating", "cost", "votes"]].reset_index(drop=True)

    df.to_parquet(OUTPUT_PATH, index=False)
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    logger.info(f"Saved to {OUTPUT_PATH}  ({size_kb:.1f} KB, {len(df)} restaurants)")


if __name__ == "__main__":
    build()
