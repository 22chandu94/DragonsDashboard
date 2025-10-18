import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df_batting = pd.read_csv("final_batting_data.csv")
df_bowling = pd.read_csv("final_bowling_data.csv")

st.title("🏏 SPVGG Dragons - Team Overview")
# TEAM SUMMARY METRICS
st.subheader("BATTING")
total_runs = df_batting["Runs"].sum()
total_matches = df_batting["Matches"].max()
total_4s = df_batting["4s"].sum()
total_6s = df_batting["6s"].sum()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Runs", total_runs)
col2.metric("Matches Played", total_matches)
col3.metric("Total 4s", total_4s)
col4.metric("Total 6s", total_6s)

st.subheader("BOWLING")
total_wickets = df_bowling["Wickets"].sum()
total_runs = df_bowling["Runs Conceded"].sum()
avg_economy = df_bowling["Economy"].mean()
total_overs = df_bowling["Overs Bowled"].sum()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Wickets", total_wickets)
col2.metric("Total Runs Conceded", total_runs)
col3.metric("Avg Economy", round(avg_economy, 2))
col4.metric("Overs Bowled", total_overs)

# DONUT CHART - RUNS CONTRIBUTION
st.subheader("🎯 Run Contribution by Player")
top_scorers = df_batting[df_batting["Runs"] > 0].sort_values(by="Runs", ascending=False)
fig1 = px.pie(
    top_scorers,
    names="Name",
    values="Runs",
    title="Total Runs Scored by Each Player",
    color_discrete_sequence=px.colors.sequential.Blues,
    hole=0.4
)
fig1.update_layout(xaxis_title="", yaxis_title="Runs", showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📋 Top 10 Run Scorers")
st.dataframe(top_scorers[["Name", "Runs", "Average", "Strike Rate"]].head(10))

st.subheader("🎯 Top Wicket-Takers")

top_wickets = df_bowling.sort_values("Wickets", ascending=False).head(10)
fig = px.pie(
    top_wickets,
    names="Player Name",
    values="Wickets",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Reds,
    title="Top Wicket-Takers of the season"
)
fig.update_layout(xaxis_title="", yaxis_title="Total Wickets", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Top 10 Wicket Takers")
st.dataframe(df_bowling[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]].head(10), use_container_width=True)