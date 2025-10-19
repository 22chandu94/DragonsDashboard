# pages/Search_Player.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Load Data ---
#@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    batting_path = os.path.join(base_dir, "../final_batting_data.csv")
    bowling_path = os.path.join(base_dir, "../final_bowling_data.csv")
    fielding_path = os.path.join(base_dir, "../final_fielding_data.csv")

    batting_df = pd.read_csv(batting_path)
    bowling_df = pd.read_csv(bowling_path)
    fielding_df = pd.read_csv(fielding_path)

    # Optional: remove players with zero dismissals
    fielding_df = fielding_df[fielding_df["Total Dismissals"] > 0]

    return batting_df, bowling_df, fielding_df

batting_df, bowling_df, fielding_df = load_data()

# --- Page Title ---
st.title("🔍 Search Player")

# --- Player Search ---
all_players = sorted(
    set(batting_df["Name"].dropna().unique()) |
    set(bowling_df["Player Name"].dropna().unique()) |
    set(fielding_df["Player Name"].dropna().unique())
)
selected_player = st.selectbox("Select a player", options=all_players)

if selected_player:
    view_type = st.radio(
        "Choose Stats Type",
        ["Batting Stats", "Bowling Stats", "Fielding Stats"],
        horizontal=True
    )

    # ------------------ Batting Stats ------------------
    if view_type == "Batting Stats":
        player_data = batting_df[batting_df["Name"] == selected_player]
        if not player_data.empty:
            st.subheader(f"🏏 Batting Stats for {selected_player}")

            # Summary Cards
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Matches", int(player_data["Matches"].max()))
            col2.metric("Runs", int(player_data["Runs"].sum()))
            col3.metric("Average", round(player_data["Average"].mean(), 2))
            col4.metric("Strike Rate", round(player_data["Strike Rate"].mean(), 2))

            col5, col6, col7, col8 = st.columns(4)
            col5.metric("Highest Score", int(player_data["Highest"].max()))
            col6.metric("4s", int(player_data["4s"].sum()))
            col7.metric("6s", int(player_data["6s"].sum()))
            col8.metric("50s", int(player_data["50s"].sum()))

            # Visuals
            metrics = ["Runs", "4s", "6s", "Average", "Strike Rate"]
            values = [
                player_data["Runs"].iloc[0],
                player_data["4s"].iloc[0],
                player_data["6s"].iloc[0],
                player_data["Average"].iloc[0],
                player_data["Strike Rate"].iloc[0],
            ]
            viz_df = pd.DataFrame({"Metric": metrics, "Value": values})

            fig = px.bar(
                viz_df,
                x="Metric",
                y="Value",
                text_auto=True,
                color="Value",
                color_continuous_scale="Blues",
                title=f"Performance Snapshot for {selected_player}",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No batting data found for {selected_player}")

    # ------------------ Bowling Stats ------------------
    elif view_type == "Bowling Stats":
        player_data = bowling_df[bowling_df["Player Name"] == selected_player]
        if not player_data.empty:
            st.subheader(f"🎯 Bowling Stats for {selected_player}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Matches", int(player_data["Matches"].max()))
            col2.metric("Wickets", int(player_data["Wickets"].sum()))
            col3.metric("Economy", round(player_data["Economy"].mean(), 2))
            col4.metric("Strike Rate", round(player_data["Strike Rate"].mean(), 2))

            col5, col6, col7, col8 = st.columns(4)
            col5.metric("Average", round(player_data["Average"].mean(), 2))
            col6.metric("Best Bowling", player_data["Best Bowling"].iloc[0])
            col7.metric("Overs Bowled", round(player_data["Overs Bowled"].sum(), 1))
            col8.metric("Maidens", int(player_data["Maidens"].sum()))

            metrics = ["Wickets", "Economy", "Strike Rate", "Average"]
            values = [
                player_data["Wickets"].iloc[0],
                player_data["Economy"].iloc[0],
                player_data["Strike Rate"].iloc[0],
                player_data["Average"].iloc[0],
            ]
            viz_df = pd.DataFrame({"Metric": metrics, "Value": values})

            fig = px.bar(
                viz_df,
                x="Metric",
                y="Value",
                text_auto=True,
                color="Value",
                color_continuous_scale="Reds",
                title=f"Performance Snapshot for {selected_player}",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No bowling data found for {selected_player}")

    # ------------------ Fielding Stats ------------------
    elif view_type == "Fielding Stats":
        player_data = fielding_df[fielding_df["Player Name"] == selected_player]
        if not player_data.empty:
            st.subheader(f"🧤 Fielding Stats for {selected_player}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Matches", int(player_data["Matches"].max()))
            col2.metric("Catches", int(player_data["Catches"].sum() + player_data["Caught Behind"].sum()))
            col3.metric("Run Outs", int(player_data["Run Outs"].sum()))
            col4.metric("Stumpings", int(player_data["Stumpings"].sum()))

            st.metric("Total Dismissals", int(player_data["Total Dismissals"].sum()))

            # Visuals
            metrics = ["Catches", "Run Outs", "Stumpings", "Total Dismissals"]
            values = [
                int(player_data["Catches"].sum() + player_data["Caught Behind"].sum()),
                int(player_data["Run Outs"].sum()),
                int(player_data["Stumpings"].sum()),
                int(player_data["Total Dismissals"].sum()),
            ]
            viz_df = pd.DataFrame({"Metric": metrics, "Value": values})

            fig = px.bar(
                viz_df,
                x="Metric",
                y="Value",
                text_auto=True,
                color="Value",
                color_continuous_scale="Greens",
                title=f"Fielding Snapshot for {selected_player}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No fielding data found for {selected_player}")
