# pages/Fielding.py
import streamlit as st
import pandas as pd
import os
from modules.player_fielding import show_player_fielding

#@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "../final_fielding_data.csv")
    df = pd.read_csv(csv_path)
    # Remove players with zero dismissals
    df = df[df["Total Dismissals"] > 0]
    return df

df = load_data()

st.title("🧤 Fielding Insights")
show_player_fielding(df)
