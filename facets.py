import streamlit as st
import json
import os
import base64

# --- DATASETS ---
try:
    with open("race-results.json") as f:
        race_data = json.load(f)
    with open("draft-results.json") as f:
        auction_data = json.load(f)
except Exception as e:
    st.error(f"Make sure your JSON files exist: {e}")
    st.stop()

# Map points from the latest race (index 0)
points_map = {item['driver']: item['points'] for item in race_data[0]['results']}

# --- HELPER: Image to Base64 ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- STREAMLIT UI SETUP ---
st.set_page_config(layout="wide", page_title="F1 Auction 2026")

# Global CSS for the card structure
st.markdown("""
    <style>
    .driver-card {
        position: relative;
        height: 450px;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .driver-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: top;
        filter: brightness(0.7) contrast(1.1);
    }
    .driver-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px;
        /* The background gradient will be injected dynamically per owner */
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
    }
    .points-badge {
        background: rgba(255,255,255,0.2);
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: bold;
    }
    .cost-text {
        font-family: monospace;
        font-size: 1.2rem;
        color: #00ff88; /* Neon green for money */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏎️ 2026 F1 Driver Auction Dashboard")

# --- FILTERS ---
owners = ["All"] + list(set(d['winner'] for d in auction_data))
selected_owner = st.sidebar.selectbox("Filter by Owner", owners)

# Filter the data
display_data = auction_data
if selected_owner != "All":
    display_data = [d for d in auction_data if d['winner'] == selected_owner]

# --- GRID DISPLAY ---
cols_per_row = 4
rows = [display_data[i:i + cols_per_row] for i in range(0, len(display_data), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for i, driver in enumerate(row):
        with cols[i]:
            points = points_map.get(driver['driver'], 0)
            img_b64 = get_base64_image(f"driver-pics/{driver['driver']}.png")
            
            # --- DYNAMIC STYLING ---
            # Devika = Purple-ish tint, Brandon = Green-ish tint
            if driver['winner'].lower() == "devika":
                overlay_color = "linear-gradient(transparent, rgba(75, 0, 130, 0.95))"
                border_color = "#9370DB"
            elif driver['winner'].lower() == "brandon":
                overlay_color = "linear-gradient(transparent, rgba(0, 50, 0, 0.95))"
                border_color = "#2E8B57"
            else:
                overlay_color = "linear-gradient(transparent, rgba(0, 0, 0, 0.9))"
                border_color = "#333"

            bg_src = f"data:image/png;base64,{img_b64}" if img_b64 else "https://via.placeholder.com/400x600/222/555?text=No+Photo"
            
            # --- HTML INJECTION ---
            st.markdown(f"""
                <div class="driver-card" style="border-bottom: 5px solid {border_color};">
                    <img class="driver-img" src="{bg_src}">
                    <div class="driver-overlay" style="background: {overlay_color};">
                        <div style="font-size: 0.7rem; opacity: 0.7; text-transform: uppercase;">Owner: {driver['winner']}</div>
                        <h2 style="margin: 0; font-size: 1.8rem; letter-spacing: -1px;">{driver['driver']}</h2>
                        <div class="stat-row">
                            <div class="points-badge">{points} PTS</div>
                            <div class="cost-text">${driver['amount_paid']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Footer info
if not display_data:
    st.warning("No drivers found for this owner.")