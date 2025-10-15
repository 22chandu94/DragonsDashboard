# pages/Batting.py
import streamlit as st
import pandas as pd
import os

from modules.player_stats import show_player_stats

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "../final_data.csv")
    return pd.read_csv(csv_path)

df = load_data()

# Page title
st.title("🏏 Batting Insights")

# Choose sub-section
section = st.radio("Select Batting View", ["Player Stats"], horizontal=True)

# Load appropriate section
if section == "Player Stats":
    show_player_stats(df)
