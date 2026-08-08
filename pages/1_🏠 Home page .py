import streamlit as st
import plotly.express as px
import pandas as pd  # Moved import here for cleaner structure
from theme_manager import apply_global_theme

# ----------------------------------------------------
# 1. Page Configuration (Must Be the Absolute First Command)
# ----------------------------------------------------
st.set_page_config(
    page_title="Military Intelligence Dashboard",
    page_icon="🏠",
    layout="wide"
)

# Run your global style helper right after configuring the page window canvas
apply_global_theme()

st.title("🏠 Home")

# ----------------------------------------------------
# 2. Optimized Data Loading Architecture (Parquet Updated)
# ----------------------------------------------------
@st.cache_data
def load_optimized_home_data():
    # Read the ultra-lightweight parquet file instantly from memory
    return pd.read_parquet("dataloader/globalterrorismdb_small.parquet")

df = load_optimized_home_data()

# ----------------------------------------------------
# 3. Dynamic Summary Metrics 
# ----------------------------------------------------
st.subheader("Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Incidents", f"{len(df):,}")
c2.metric("Fatalities", f"{int(df['nkill'].fillna(0).sum()):,}")
c3.metric("Injured", f"{int(df['nwound'].fillna(0).sum()):,}")
c4.metric("Countries", f"{df['country_txt'].nunique():,}")

st.divider()

# ----------------------------------------------------
# 4. Attack Volume Linear Progression
# ----------------------------------------------------
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

# FIXED: Replaced invalid width="stretch" with native container width scaling
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------------------------------
# 5. User Direction Footers
# ----------------------------------------------------
st.success("👉 Click **Global Threat Map** from the left sidebar to explore incidents geographically.")
st.markdown("<p style='color: red; font-size: 0.9rem; font-style: italic; margin-top: 5px;'>💡 <b>Note:</b> You may experience a small initialization delay while loading the different layers for the first time.</p>", unsafe_allow_html=True)
