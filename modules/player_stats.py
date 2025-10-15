# modules/player_stats.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show_player_stats(df):
    st.header("⚡ Player Performance Leaderboards")

    st.subheader("📊 Batting Average Comparison")

    min_innings = st.slider("Minimum Innings", min_value=0, max_value=30, value=5)
    filtered_df = df[df["innings"] >= min_innings]
    sorted_df = filtered_df.sort_values(by="average", ascending=False)

    fig = px.bar(
        sorted_df,
        x="name",
        y="average",
        title=f"Batting Averages (Min {min_innings} Innings)",
        text_auto=".2f",
        labels={"average": "Batting Average", "name": "Player"},
        color="average",
        color_continuous_scale="Blues"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("See Data Table"):
        st.dataframe(sorted_df[["name", "innings", "average", "total_runs", "strike_rate"]])

    # --- Strike Rate Leaderboard ---
    st.subheader("🔥 Strike Rate Leaderboard")
    sr_df = df[df["ball_faced"] > 0].copy().sort_values(by="strike_rate", ascending=False)
    fig_sr = px.bar(sr_df, x="name", y="strike_rate", color="strike_rate", text_auto=".1f", color_continuous_scale="OrRd")
    fig_sr.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sr, use_container_width=True)
    with st.expander("See Data Table"):
        st.dataframe(sr_df[["name", "strike_rate", "ball_faced", "total_runs"]])

    # --- Boundary % ---
    st.subheader("🎯 Boundary Percentage Analysis")
    boundary_df = df.copy()
    boundary_df["total_boundaries"] = boundary_df["4s"] + boundary_df["6s"]
    boundary_df["boundary_runs"] = boundary_df["4s"] * 4 + boundary_df["6s"] * 6
    boundary_df["boundary_%"] = (boundary_df["boundary_runs"] / boundary_df["total_runs"]) * 100
    boundary_df = boundary_df.replace([float('inf'), -float('inf')], 0).fillna(0)
    boundary_df = boundary_df.sort_values(by="boundary_%", ascending=False)
    fig_bp = px.bar(boundary_df[boundary_df["total_runs"] > 0], x="name", y="boundary_%", color="boundary_%", text_auto=".1f", color_continuous_scale="Viridis")
    fig_bp.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bp, use_container_width=True)
    with st.expander("See Boundary % Table"):
        st.dataframe(boundary_df[["name", "total_runs", "4s", "6s", "boundary_runs", "boundary_%"]])

    # --- Total 4s + 6s ---
    st.subheader("💥 4s + 6s Leaderboard")
    boundary_leader_df = df.copy()
    boundary_leader_df["total_boundaries"] = boundary_leader_df["4s"] + boundary_leader_df["6s"]
    boundary_leader_df = boundary_leader_df.sort_values(by="total_boundaries", ascending=False)
    fig_combo = px.bar(boundary_leader_df, x="name", y="total_boundaries", color="total_boundaries", text_auto=True, color_continuous_scale="Tealgrn")
    fig_combo.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_combo, use_container_width=True)
    with st.expander("See 4s + 6s Table"):
        st.dataframe(boundary_leader_df[["name", "4s", "6s", "total_boundaries"]])
