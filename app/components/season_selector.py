"""Season selector sidebar component."""

import streamlit as st
from app.data import available_seasons


def render_season_selector() -> int:
    """Render a sidebar selectbox for season year.

    Returns:
        Selected season year as int.
    """
    seasons = available_seasons()
    default = max(seasons) if seasons else None
    selected = st.sidebar.selectbox(
        "Season",
        options=seasons,
        index=seasons.index(default) if default in seasons else 0,
        format_func=lambda y: str(y),
    )
    return selected
