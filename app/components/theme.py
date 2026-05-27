"""F1 red theme injection for iframe embed."""

import streamlit as st

F1_RED = "#e10600"
F1_DARK_BG = "#1a1a1a"
F1_CARD_BG = "#2d2d2d"
F1_TEXT = "#ffffff"

_THEME_CSS = """
<style>
/* Hide Streamlit toolbar / hamburger menu */
header[data-testid="stHeader"] {
    display: none !important;
}
#MainMenu {
    visibility: hidden !important;
}
footer {
    visibility: hidden !important;
}

/* Dark background */
.stApp {
    background-color: #1a1a1a;
    color: #ffffff;
}

/* F1 red accents on metrics */
[data-testid="metric-container"] {
    background-color: #2d2d2d;
    border-left: 4px solid #e10600;
    border-radius: 6px;
    padding: 8px 12px;
}

/* F1 red divider replacement */
hr {
    border-color: #e10600 !important;
    opacity: 0.6;
}

/* Sidebar dark */
[data-testid="stSidebar"] {
    background-color: #111111;
}

/* Title accent */
h1, h2, h3 {
    color: #ffffff;
}

/* Selectbox / dropdown dark */
[data-testid="stSelectbox"] > div {
    background-color: #2d2d2d;
}
</style>
"""


def inject_theme() -> None:
    """Inject F1 red dark theme CSS once per page load."""
    st.markdown(_THEME_CSS, unsafe_allow_html=True)
