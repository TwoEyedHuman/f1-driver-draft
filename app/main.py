"""F1 Driver Draft Dashboard — entry point."""

import streamlit as st

from app.data import load_season
from app.standings import build_standings
from app.components.season_selector import render_season_selector
from app.components.driver_card import inject_card_css, render_driver_card
from app.components.theme import inject_theme

st.set_page_config(layout="wide", page_title="F1 Auction 2026")

inject_theme()
inject_card_css()

# --- Sidebar controls ---
year = render_season_selector()
df = load_season(year)

owners = ["All Owners"] + sorted(df["winner"].unique().tolist())
selected_owner = st.sidebar.selectbox("Filter by Owner", owners)

# --- Header ---
st.title("🏎️ 2026 F1 Driver Auction Dashboard")

# --- Leaderboard ---
st.subheader("Current Standings")
summary = build_standings(df)
l_cols = st.columns(len(summary))
for idx, row in summary.iterrows():
    l_cols[idx].metric(
        f"Team {row['winner']}",
        f"{row['points']} PTS",
        f"Spend: ${row['amount_paid']}",
    )

st.divider()

# --- Driver grid ---
filtered_df = df if selected_owner == "All Owners" else df[df["winner"] == selected_owner]

cols_per_row = 4
rows_data = filtered_df.to_dict("records")
rows = [rows_data[i : i + cols_per_row] for i in range(0, len(rows_data), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row)
    for i, driver in enumerate(row):
        with cols[i]:
            render_driver_card(driver)
