import streamlit as st
import plotly.express as px

from theme_manager import apply_global_theme
from dataloader.data_loader import load_data

st.set_page_config(
    page_title="Military Intelligence Dashboard",
    page_icon="🏠",
    layout="wide"
)

apply_global_theme()

st.title("🏠 Home")

df = load_data()

st.subheader("Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{len(df):,}"
)

c2.metric(
    "Fatalities",
    f"{int(df['nkill'].fillna(0).sum()):,}"
)

c3.metric(
    "Injured",
    f"{int(df['nwound'].fillna(0).sum()):,}"
)

c4.metric(
    "Countries",
    f"{df['country_txt'].nunique():,}"
)

st.divider()

st.subheader("Attacks Over Years")

yearly = (
    df.groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

fig = px.line(
    yearly,
    x="iyear",
    y="Attacks",
    markers=True
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

st.success(
    "👉 Click **Global Threat Map** from the left sidebar "
    "to explore incidents geographically."
)

st.markdown(
    "💡 Note: You may experience a small initialization delay "
    "while loading the different layers for the first time."
)