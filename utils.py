import pandas as pd
import json
import os
import base64
import streamlit as st


def load_data():
    with open("race-results.json") as f:
        race_json = json.load(f)
    with open("draft-results.json") as f:
        auction_json = json.load(f)

    all_race_results = []
    for race in race_json:
        all_race_results.extend(race['results'])
    
    df_all_points = pd.DataFrame(all_race_results)
    df_totals = df_all_points.groupby('driver')['points'].sum().reset_index()

    df_auction = pd.DataFrame(auction_json)

    df = pd.merge(df_auction, df_totals, on="driver", how="left")
    
    df['points'] = df['points'].fillna(0).astype(int)
    df = df.sort_values(by="driver")
    
    return df

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None