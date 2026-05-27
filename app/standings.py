"""Standings table logic — aggregates per-owner stats."""

import pandas as pd


def build_standings(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate driver data into owner standings.

    Args:
        df: Season DataFrame from data.load_season()

    Returns:
        DataFrame with columns: winner, points, amount_paid, roi
        Sorted by points descending.
    """
    summary = (
        df.groupby("winner")
        .agg(points=("points", "sum"), amount_paid=("amount_paid", "sum"))
        .reset_index()
    )
    summary["roi"] = (
        summary["points"] / summary["amount_paid"].replace(0, 1)
    ).round(2)
    summary = summary.sort_values("points", ascending=False).reset_index(drop=True)
    return summary
