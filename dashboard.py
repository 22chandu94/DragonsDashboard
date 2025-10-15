import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("final_data.csv")

# Sidebar - Select Player
player_names = df["name"].sort_values().unique()
selected_player = st.sidebar.selectbox("Select a Player", player_names)

# Filter data
player_data = df[df["name"] == selected_player].squeeze()

# Title
st.title(f"{selected_player} - Batting Performance")

# Key Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Runs", player_data["total_runs"])
col2.metric("Average", round(player_data["average"], 2))
col3.metric("Strike Rate", round(player_data["strike_rate"], 2))

# Visual - Boundary Breakdown
st.subheader("Boundary Breakdown")
fig = px.pie(
    names=["Fours", "Sixes"],
    values=[player_data["4s"], player_data["6s"]],
    title="Fours vs Sixes"
)
st.plotly_chart(fig)

# More Stats
st.subheader("Detailed Stats")
st.dataframe(player_data.to_frame().T)
