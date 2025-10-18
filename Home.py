import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df_batting = pd.read_csv("final_batting_data.csv")
df_bowling = pd.read_csv("final_bowling_data.csv")
df_fielding = pd.read_csv("final_fielding_data.csv")

st.title("🐉 SPVGG Dragons - Team Overview")
# TEAM SUMMARY METRICS
st.subheader("🏏 BATTING")
total_runs = df_batting["Runs"].sum()
total_matches = df_batting["Matches"].max()
total_4s = df_batting["4s"].sum()
total_6s = df_batting["6s"].sum()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Runs", total_runs)
col2.metric("Matches Played", total_matches)
col3.metric("Total 4s", total_4s)
col4.metric("Total 6s", total_6s)

st.subheader("⚾ BOWLING")
total_wickets = df_bowling["Wickets"].sum()
total_runs = df_bowling["Runs Conceded"].sum()
avg_economy = df_bowling["Economy"].mean()
total_overs = df_bowling["Overs Bowled"].sum()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Wickets", total_wickets)
col2.metric("Total Runs Conceded", total_runs)
col3.metric("Avg Economy", round(avg_economy, 2))
col4.metric("Overs Bowled", total_overs)

st.subheader("🧤 FIELDING")
total_catches = (df_fielding["Catches"] + df_fielding["Caught Behind"]).sum()
total_run_outs = df_fielding["Run Outs"].sum()
total_stumpings = df_fielding["Stumpings"].sum()
total_dismissals = df_fielding["Total Dismissals"].sum()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Catches", total_catches)
col2.metric("Total Run Outs", total_run_outs)
col3.metric("Total Stumpings", total_stumpings)
col4.metric("Total Dismissals", total_dismissals)

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
top_scorers_table = top_scorers[["Name", "Runs", "Average", "Strike Rate"]].head(10).reset_index(drop=True)
top_scorers_table.index += 1  # Start index from 1
top_scorers_table.index.name = "Rank"  # Optional: give a name to the index column
st.dataframe(top_scorers_table)

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
top_wickets_table = df_bowling[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]].head(10).reset_index(drop=True)
top_wickets_table.index += 1  # Start index from 1
top_wickets_table.index.name = "Rank"  # Optional: add a name to the index column
st.dataframe(top_wickets_table, use_container_width=True)

# --- FIELDING SECTION ---

# Donut Chart - Dismissal Contribution
st.subheader("🎯 Dismissal Contribution by Player")
top_fielders = df_fielding[df_fielding["Total Dismissals"] > 0].sort_values(
    by="Total Dismissals", ascending=False
)
fig1 = px.pie(
    top_fielders,
    names="Player Name",
    values="Total Dismissals",
    hole=0.4,
    title="Total Dismissals by Each Player",
    color_discrete_sequence=px.colors.sequential.Greens,
)
fig1.update_layout(xaxis_title="", yaxis_title="Dismissals", showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Top 10 Fielders Table
st.subheader("📋 Top 10 Fielders (by Total Dismissals)")
top_10_fielders = top_fielders.head(10).reset_index(drop=True)
top_10_fielders.index += 1  # Start index from 1
top_10_fielders.index.name = "Rank"  # Optional: name the index column

st.dataframe(
    top_10_fielders[
        ["Player Name", "Matches", "Catches", "Caught Behind", "Run Outs", "Stumpings", "Total Dismissals"]
    ],
    use_container_width=True
)

