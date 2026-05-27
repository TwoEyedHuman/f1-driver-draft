import streamlit as st
import pandas as pd
import json
import os
import base64

# --- DATA LOADING & AGGREGATION ---
def load_data():
    with open("race-results.json") as f:
        race_json = json.load(f)
    with open("draft-results.json") as f:
        auction_json = json.load(f)

    # 1. Aggregate points across all races
    all_race_results = []
    for race in race_json:
        all_race_results.extend(race['results'])
    
    # Create DataFrame and sum points by driver
    df_all_points = pd.DataFrame(all_race_results)
    df_totals = df_all_points.groupby('driver')['points'].sum().reset_index()

    # 2. Load Auction Data
    df_auction = pd.DataFrame(auction_json)

    # 3. Merge: Auction list is our "Master List"
    df = pd.merge(df_auction, df_totals, on="driver", how="left")
    
    # Clean up: Fill missing points with 0 and sort
    df['points'] = df['points'].fillna(0).astype(int)
    df = df.sort_values(by="driver")
    
    return df

df = load_data()

# --- HELPER: Image to Base64 ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- STREAMLIT UI SETUP ---
st.set_page_config(layout="wide", page_title="F1 Auction 2026")

# Global CSS for the modern "Hero Card" look
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
    """, unsafe_allow_html=True)

st.title("🏎️ 2026 F1 Driver Auction Dashboard")

# --- LEADERBOARD (Top of Page) ---
st.subheader("Current Standings")
summary = df.groupby('winner').agg({'points': 'sum', 'amount_paid': 'sum'}).reset_index()
summary['ROI (Pts/$)'] = (summary['points'] / summary['amount_paid'].replace(0, 1)).round(2)

l_cols = st.columns(len(summary))
for idx, row in summary.iterrows():
    l_cols[idx].metric(f"Team {row['winner']}", f"{row['points']} PTS", f"Spend: ${row['amount_paid']}")

st.divider()

# --- FILTERS ---
owners = ["All Owners"] + sorted(df['winner'].unique().tolist())
selected_owner = st.sidebar.selectbox("Filter by Owner", owners)

filtered_df = df
if selected_owner != "All Owners":
    filtered_df = df[df['winner'] == selected_owner]

# --- GRID DISPLAY ---
cols_per_row = 4
rows_data = filtered_df.to_dict('records')
rows = [rows_data[i:i + cols_per_row] for i in range(0, len(rows_data), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for i, driver in enumerate(row):
        with cols[i]:
            img_b64 = get_base64_image(f"driver-pics/{driver['driver']}.png")
            
            # Color Logic
            is_devika = driver['winner'].lower() == "devika"
            overlay_color = "rgba(75, 0, 130, 0.9)" if is_devika else "rgba(0, 50, 0, 0.9)"
            border_color = "#9370DB" if is_devika else "#2E8B57"

            bg_src = f"data:image/png;base64,{img_b64}" if img_b64 else "https://via.placeholder.com/400x600/222/555?text=No+Photo"
            
            st.markdown(f"""
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
                """, unsafe_allow_html=True)