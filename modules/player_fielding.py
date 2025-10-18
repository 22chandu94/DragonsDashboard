# modules/player_fielding.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show_player_fielding(df):
    st.subheader("🧤 Fielding Leaderboards")

    # Combine Catches + Caught Behind
    df['Catches'] = df['Catches'] + df['Caught Behind']

    # --- Top Catchers ---
    st.header("🏆 Top Catchers")
    top_catchers = df.sort_values("Catches", ascending=False).head(10)
    fig1 = px.bar(
        top_catchers,
        x="Player Name",
        y="Catches",
        color="Catches",
        color_continuous_scale="Blues",
        text="Catches"
    )
    fig1.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    with st.expander("See Data Table"):
        st.dataframe(top_catchers[["Player Name", "Matches", "Catches"]])

    # --- Top Total Dismissals ---
    st.header("⚡ Top Total Dismissals")
    top_dismissals = df.sort_values("Total Dismissals", ascending=False).head(10)
    fig2 = px.bar(
        top_dismissals,
        x="Player Name",
        y="Total Dismissals",
        color="Total Dismissals",
        color_continuous_scale="Oranges",
        text="Total Dismissals"
    )
    fig2.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("See Data Table"):
        st.dataframe(top_dismissals[["Player Name", "Matches", "Total Dismissals"]])

    # --- Dismissals per Match ---
    st.header("📊 Dismissals per Match")
    fig3 = px.bar(
        df.sort_values("Dismissals/Match", ascending=False),
        x="Player Name",
        y="Dismissals/Match",
        color="Dismissals/Match",
        text="Dismissals/Match",
        color_continuous_scale="Teal"
    )
    fig3.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    with st.expander("See Data Table"):
        st.dataframe(df[["Player Name", "Matches", "Dismissals/Match"]])

    # --- Run Outs vs Stumpings ---
    st.header("🔄 Run Outs & Stumpings Breakdown")
    fig4 = px.bar(
        df,
        x="Player Name",
        y=["Run Outs", "Assist Run Outs", "Stumpings"],
        text_auto=True,
        title="Run Outs and Stumpings by Player"
    )
    fig4.update_layout(barmode="stack", xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

    # --- Catches vs Total Dismissals Scatter ---
    st.header("⚖️ Catches vs Total Dismissals")
    fig5 = px.scatter(
        df,
        x="Catches",
        y="Total Dismissals",
        size="Matches",
        color="Player Name",
        hover_data=["Player Name", "Matches"],
        title="Catches vs Total Dismissals"
    )
    st.plotly_chart(fig5, use_container_width=True)
