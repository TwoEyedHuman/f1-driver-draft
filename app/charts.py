"""Plotly chart rendering for F1 driver draft dashboard.

Note: plotly is not yet in requirements.txt — add it when charts are wired
into main.py (Story 1.x).
"""

from __future__ import annotations

import pandas as pd


def points_bar_chart(df: pd.DataFrame):  # -> go.Figure once plotly added
    """Bar chart of points per driver, coloured by owner.

    Args:
        df: Season DataFrame from data.load_season()

    Returns:
        Plotly Figure.
    """
    import plotly.express as px  # deferred import until plotly is in deps

    fig = px.bar(
        df.sort_values("points", ascending=False),
        x="driver",
        y="points",
        color="winner",
        labels={"driver": "Driver", "points": "Points", "winner": "Owner"},
        title="Points by Driver",
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig
