"""Driver hero card component."""

import os
import base64

import streamlit as st


_PICS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "driver-pics")

_CARD_CSS = """
<style>
.driver-card {
    position: relative;
    height: 450px;
    border-radius: 15px;
    overflow: hidden;
    margin-bottom: 25px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    color: white;
}
.driver-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top;
    filter: brightness(0.7);
}
.driver-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}
.points-badge {
    background: rgba(255,255,255,0.2);
    padding: 4px 12px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.1rem;
}
</style>
"""


def inject_card_css() -> None:
    """Inject driver card CSS once per page load."""
    st.markdown(_CARD_CSS, unsafe_allow_html=True)


def _get_base64_image(driver_name: str) -> str | None:
    path = os.path.join(_PICS_DIR, f"{driver_name}.png")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def render_driver_card(driver: dict) -> None:
    """Render a single driver hero card into the current Streamlit column.

    Args:
        driver: Dict with keys: driver, winner, amount_paid, points.
    """
    img_b64 = _get_base64_image(driver["driver"])
    is_devika = driver["winner"].lower() == "devika"
    overlay_color = "rgba(75, 0, 130, 0.9)" if is_devika else "rgba(0, 50, 0, 0.9)"
    border_color = "#9370DB" if is_devika else "#2E8B57"
    bg_src = (
        f"data:image/png;base64,{img_b64}"
        if img_b64
        else "https://via.placeholder.com/400x600/222/555?text=No+Photo"
    )

    st.markdown(
        f"""
        <div class="driver-card" style="border-bottom: 5px solid {border_color};">
            <img class="driver-img" src="{bg_src}">
            <div class="driver-overlay" style="background: linear-gradient(transparent, {overlay_color});">
                <div style="font-size: 0.75rem; opacity: 0.8; text-transform: uppercase; font-weight: bold;">{driver['winner']}</div>
                <h2 style="margin: 0; font-size: 2rem; letter-spacing: -1px;">{driver['driver']}</h2>
                <div class="stat-row">
                    <div class="points-badge">{driver['points']} PTS</div>
                    <div style="font-family: monospace; color: #00ff88; font-size: 1.3rem;">${driver['amount_paid']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
