import streamlit as st
import pandas as pd
import plotly.express as px
import os

#@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "../final_bowling_data.csv")
    return pd.read_csv(csv_path)

df = load_data()

st.title("🏏 Bowling Insights")
st.subheader("💰 Best Economy Rates (Min 10 Overs)")

eco_df = df[df["Overs Bowled"] >= 10].sort_values("Economy", ascending=True).head(10)
fig = px.bar(
    eco_df,
    x="Player Name",
    y="Economy",
    color="Economy",
    color_continuous_scale="Greens_r",
    text="Economy",
)
fig.update_layout(xaxis_title="", yaxis_title="Economy", showlegend=False)
st.plotly_chart(fig, use_container_width=True)
with st.expander("See Data Table"):
    st.dataframe(df[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]], use_container_width=True)


st.subheader("⚡ Bowling Strike Rate Leaders (Min 5 Wickets)")

sr_df = df[df["Wickets"] >= 5].sort_values("Strike Rate", ascending=True).head(10)
fig = px.bar(
    sr_df,
    x="Player Name",
    y="Strike Rate",
    color="Strike Rate",
    color_continuous_scale="Oranges_r",
    text="Strike Rate",
)
fig.update_layout(xaxis_title="", yaxis_title="Balls per Wicket", showlegend=False)
st.plotly_chart(fig, use_container_width=True)
with st.expander("See Data Table"):
    st.dataframe(df[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]], use_container_width=True)


st.subheader("🎨 Wickets vs Economy (Balance of Attack and Control)")

fig = px.scatter(
    df,
    x="Economy",
    y="Wickets",
    size="Overs Bowled",
    color="Bowling Style",
    hover_name="Player Name",
    title="Wickets vs Economy",
)
st.plotly_chart(fig, use_container_width=True)
with st.expander("See Data Table"):
    st.dataframe(df[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]], use_container_width=True)


st.subheader("📊 Overs Bowled vs Wickets (Bubble Chart)")

fig5 = px.scatter(
    df,
    x="Overs Bowled",
    y="Wickets",
    size="Economy",
    color="Player Name",
    hover_data=["Economy", "Strike Rate", "Bowling Style"],
    size_max=25,
    height=500,
)

fig5.update_layout(
    xaxis_title="Overs Bowled",
    yaxis_title="Total Wickets",
    showlegend=False,
    title="Overs Bowled vs Wickets (Bubble Representation)"
)

st.plotly_chart(fig5, use_container_width=True)
with st.expander("See Data Table"):
    st.dataframe(df[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]], use_container_width=True)


st.subheader("🌀 Bowling Style Distribution")

style_counts = df["Bowling Style"].value_counts().reset_index()
style_counts.columns = ["Bowling Style", "Count"]

fig = px.pie(
    style_counts,
    names="Bowling Style",
    values="Count",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig, use_container_width=True)
with st.expander("See Data Table"):
    st.dataframe(df[["Player Name", "Overs Bowled", "Wickets", "Economy", "Strike Rate", "Average", "Bowling Style"]], use_container_width=True)


