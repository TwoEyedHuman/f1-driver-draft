"""Plotly chart rendering for F1 driver draft dashboard.

Note: plotly is not yet in requirements.txt — add it when charts are wired
into main.py (Story 1.x).
"""

from __future__ import annotations

import pandas as pd

# F1 brand colours — matches theme.py
_F1_RED = "#e10600"
_CHART_BG = "#1a1a1a"
_CHART_PAPER = "#2d2d2d"
_CHART_TEXT = "#ffffff"

_OWNER_COLORS = [
    _F1_RED,
    "#ffffff",
    "#ff8c00",
    "#00cfff",
    "#a3ff00",
    "#bf5fff",
]


def points_bar_chart(df: pd.DataFrame):  # -> go.Figure once plotly added
    """Bar chart of points per driver, coloured by owner.

    Args:
        df: Season DataFrame from data.load_season()

    Returns:
        Plotly Figure with F1 dark theme applied.
    """
    import plotly.express as px  # deferred import until plotly is in deps

    owners = sorted(df["winner"].unique().tolist())
    color_map = {owner: _OWNER_COLORS[i % len(_OWNER_COLORS)] for i, owner in enumerate(owners)}

    fig = px.bar(
        df.sort_values("points", ascending=False),
        x="driver",
        y="points",
        color="winner",
        color_discrete_map=color_map,
        labels={"driver": "Driver", "points": "Points", "winner": "Owner"},
        title="Points by Driver",
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor=_CHART_BG,
        paper_bgcolor=_CHART_PAPER,
        font_color=_CHART_TEXT,
        title_font_color=_F1_RED,
        legend_bgcolor=_CHART_PAPER,
        xaxis=dict(gridcolor="#444444"),
        yaxis=dict(gridcolor="#444444"),
    )
    return fig
