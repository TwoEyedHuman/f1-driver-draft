import streamlit as st
from utils import load_data, local_css, get_base64_image

df = load_data()

# --- STREAMLIT UI SETUP ---
st.set_page_config(layout="wide", page_title="F1 Auction 2026")
local_css("style.css")

st.title("🏎️ 2026 F1 Driver Auction Dashboard")

# --- LEADERBOARD (Top of Page) ---
st.subheader("Current Standings")
summary = df.groupby('winner').agg({'points': 'sum', 'amount_paid': 'sum'}).reset_index()

l_cols = st.columns(len(summary))
for idx, row in summary.iterrows():
    owner = row['winner']
    # Get logo for the summary
    logo_b64 = get_base64_image(f"team-logos/{owner.lower()}-primary.png")
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 180px; margin-top: 10px;">' if logo_b64 else f"<h3>{owner}</h3>"
    
    with l_cols[idx]:
        with st.container(border=True):
            st.markdown(f"""
                <div style="text-align: center;">
                    {logo_html}
                    <div style="font-size: 1.5rem; font-weight: bold;">{row['points']} <small>PTS</small></div>
                    <div style="color: #888; font-size: 0.9rem;">Spend: ${row['amount_paid']}</div>
                </div>
                """, unsafe_allow_html=True)

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
            team_logo_b64 = get_base64_image(f"team-logos/{driver['winner'].lower()}-primary.png")
            
            is_devika = driver['winner'].lower() == "devika"
            overlay_color = "rgba(75, 0, 130, 0.9)" if is_devika else "rgba(0, 50, 0, 0.9)"
            border_color = "#9370DB" if is_devika else "#2E8B57"
            bg_src = f"data:image/png;base64,{img_b64}" if img_b64 else "https://via.placeholder.com/400x600"
            
            # The HTML block - strictly mapped to one st.markdown call
            card_html = f"""
                <div class="driver-card" style="border-bottom: 5px solid {border_color};">
                    <img src="data:image/png;base64,{team_logo_b64}" class="team-logo-corner">
                    <img class="driver-img" src="{bg_src}">
                    <div class="driver-overlay" style="background: linear-gradient(transparent, {overlay_color});">
                        <h2 style="margin: 0; font-size: 2rem; letter-spacing: -1px; color: white;">{driver['driver']}</h2>
                        <div class="stat-row">
                            <div class="points-badge">{driver['points']} PTS</div>
                            <div style="font-family: monospace; color: #00ff88; font-size: 1.3rem; font-weight: bold;">${driver['amount_paid']}</div>
                        </div>
                    </div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)