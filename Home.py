import streamlit as st

st.set_page_config(
    page_title="AI Military Intelligence Dashboard",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 Military Intelligence Dashboard & Forecasting Portal")
st.markdown(
    "<p style='color: purple ; font-size: 1.3rem; margin-top: -15px;'> Real-time operational & threat forecasting dashboard</p>", 
    unsafe_allow_html=True
)

st.markdown("""
### Welcome

This dashboard provides military intelligence analysis using the
Global Terrorism Database (GTD).

👈 Select a page from the sidebar.
""")

st.info("""
Available Modules

- 🏠 Home
- 🌍 Global Threat Map
- 🌎 Country Analysis
- 🤖 Attack Prediction
- 🚨 Threat Level Prediction
- 📈 Forecasting
- 🧠 AI Intelligence Report
- 📊 Data Explorer
- ⚙ Settings

👈  Please Use the **left sidebar** to navigate.
""")

st.info("Select a page from the sidebar to begin.")