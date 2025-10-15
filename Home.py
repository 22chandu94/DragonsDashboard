import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("final_data.csv")

# Add "All Players" option to the top of the dropdown
player_names = ["All Players"] + sorted(df["Name"].unique().tolist())
selected_player = st.sidebar.selectbox("Select a Player", player_names)

# === HOME PAGE ===
if selected_player == "All Players":
    st.title("🏏 SPVGG Dragons - Team Overview")

    # TEAM SUMMARY METRICS
    total_runs = df["Runs"].sum()
    total_matches = df["Matches"].max()
    total_4s = df["4s"].sum()
    total_6s = df["6s"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Runs", total_runs)
    col2.metric("Matches Played", total_matches)
    col3.metric("Total 4s", total_4s)
    col4.metric("Total 6s", total_6s)

    # DONUT CHART - RUNS CONTRIBUTION
    st.subheader("🎯 Run Contribution by Player")
    top_scorers = df[df["Runs"] > 0].sort_values(by="Runs", ascending=False)

    fig = px.pie(
        top_scorers,
        names="Name",
        values="Runs",
        title="Total Runs Scored by Each Player",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Top 10 Run Scorers")
    st.dataframe(top_scorers[["Name", "Runs", "Average", "Strike Rate"]].head(10))

# === PLAYER PROFILE PAGE ===
else:
    player_data = df[df["Name"] == selected_player].squeeze()

    st.title(f"{selected_player} - Batting Performance")

    # Key Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Runs", player_data["Runs"])
    col2.metric("Average", round(player_data["Average"], 2))
    col3.metric("Strike Rate", round(player_data["Strike Rate"], 2))

    # Boundary Breakdown
    st.subheader("Boundary Breakdown")
    fig = px.pie(
        names=["Fours", "Sixes"],
        values=[player_data["4s"], player_data["6s"]],
        title="Fours vs Sixes"
    )
    st.plotly_chart(fig)

    # Detailed Stats
    st.subheader("Detailed Stats")
    st.dataframe(player_data.to_frame().T)