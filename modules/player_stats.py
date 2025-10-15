# modules/player_stats.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show_player_stats(df):
    st.subheader("⚡ Player Performance Leaderboards")

    st.subheader("📊 Batting Average Comparison")

    min_innings = st.slider("Minimum Innings", min_value=0, max_value=30, value=5)
    filtered_df = df[df["Innings"] >= min_innings]
    sorted_df = filtered_df.sort_values(by="Average", ascending=False)

    fig = px.bar(
        sorted_df,
        x="Name",
        y="Average",
        title=f"Batting Averages (Min {min_innings} Innings)",
        text_auto=".2f",
        labels={"Average": "Batting Average", "Name": "Player"},
        color="Average",
        color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("See Data Table"):
        st.dataframe(sorted_df[["Name", "Innings", "Average", "Runs", "Strike Rate"]])

    # --- Strike Rate Leaderboard ---
    st.header("🔥 Strike Rate Leaderboard")
    sr_df = df[df["Balls Faced"] > 0].copy().sort_values(by="Strike Rate", ascending=False)
    fig_sr = px.bar(sr_df, x="Name", y="Strike Rate", color="Strike Rate", text_auto=".1f", color_continuous_scale="OrRd")
    fig_sr.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sr, use_container_width=True)
    with st.expander("See Data Table"):
        st.dataframe(sr_df[["Name", "Strike Rate", "Balls Faced", "Runs"]])

    # --- Boundary % ----
    st.header("🎯 Boundary Percentage Analysis")
    boundary_df = df.copy()
    boundary_df["total_boundaries"] = boundary_df["4s"] + boundary_df["6s"]
    boundary_df["boundary_runs"] = boundary_df["4s"] * 4 + boundary_df["6s"] * 6
    boundary_df["boundary_%"] = (boundary_df["boundary_runs"] / boundary_df["Runs"]) * 100
    boundary_df = boundary_df.replace([float('inf'), -float('inf')], 0).fillna(0)
    boundary_df = boundary_df.sort_values(by="boundary_%", ascending=False)
    fig_bp = px.bar(boundary_df[boundary_df["Runs"] > 0], x="Name", y="boundary_%", color="boundary_%", text_auto=".1f", color_continuous_scale="Viridis")
    fig_bp.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bp, use_container_width=True)
    with st.expander("See Boundary % Table"):
        st.dataframe(boundary_df[["Name", "Runs", "4s", "6s", "boundary_runs", "boundary_%"]])

    # --- Total 4s + 6s ---
    st.header("💥 4s + 6s Leaderboard")
    boundary_leader_df = df.copy()
    boundary_leader_df["total_boundaries"] = boundary_leader_df["4s"] + boundary_leader_df["6s"]
    boundary_leader_df = boundary_leader_df.sort_values(by="total_boundaries", ascending=False)
    fig_combo = px.bar(boundary_leader_df, x="Name", y="total_boundaries", color="total_boundaries", text_auto=True, color_continuous_scale="Tealgrn")
    fig_combo.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_combo, use_container_width=True)
    with st.expander("See 4s + 6s Table"):
        st.dataframe(boundary_leader_df[["Name", "4s", "6s", "total_boundaries"]])
