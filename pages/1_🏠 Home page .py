import streamlit as st
import plotly.express as px
from dataloader import data_loader


st.title("🏠 Home")

df = load_data()

st.subheader("Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Incidents", len(df))
c2.metric("Fatalities", int(df["nkill"].sum()))
c3.metric("Injured", int(df["nwound"].sum()))
c4.metric("Countries", df["country_txt"].nunique())

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

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.success("👉 Click **Global Threat Map** from the left sidebar to explore incidents geographically." )
st.markdown("<p style='color: red; font-size: 0.9rem; font-style: italic; margin-top: 5px;'>💡 <b>Note:</b> You may experience a small initialization delay  while loading the different layers for the first time.</p>", unsafe_allow_html=True)