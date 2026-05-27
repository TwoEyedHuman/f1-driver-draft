"""Data loading and season utilities."""

import os
import pandas as pd

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def available_seasons() -> list[int]:
    """Scan data/ for CSV files and return sorted list of season years."""
    years = []
    for fname in os.listdir(_DATA_DIR):
        if fname.endswith(".csv"):
            try:
                years.append(int(fname[:-4]))
            except ValueError:
                pass
    return sorted(years)


def load_season(year: int) -> pd.DataFrame:
    """Load season data for *year* from data/<year>.csv.

    Returns DataFrame with columns:
        driver, winner, amount_paid, points
    """
    path = os.path.join(_DATA_DIR, f"{year}.csv")
    df = pd.read_csv(path, dtype={"driver": str, "winner": str, "amount_paid": int, "points": int})
    df = df.sort_values("driver").reset_index(drop=True)
    return df
