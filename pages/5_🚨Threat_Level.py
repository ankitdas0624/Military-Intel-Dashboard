import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Threat Level Prediction", page_icon="🚨", layout="wide")
st.title("🚨 AI Threat Level Prediction System")

# ---------------------------------------------------
# 1. FIX LATENCY: Speed up data loading with Caching
# ---------------------------------------------------
@st.cache_data
def load_cached_data():
    df = pd.read_csv(
        "dataloader/globalterrorismdb_0718dist.csv",
        encoding="latin1",
        low_memory=False
    )
    return df

df = load_cached_data()

# ---------------------------------------------------
# 2. FIX NUMBERS: Load translation keys (Encoders)
# ---------------------------------------------------
encoders_path = "models/feature_encoders.pkl"

if os.path.exists(encoders_path):
    encoders = joblib.load(encoders_path)
    
    # Get actual text names from your saved encoder models
    countries = list(encoders["country_txt"].classes_)
    regions = list(encoders["region_txt"].classes_)
    attacks = list(encoders["attacktype1_txt"].classes_)
    weapons = list(encoders["weaptype1_txt"].classes_)
    targets = list(encoders["targtype1_txt"].classes_)
else:
    # Backup fallback if your encoder file isn't generated yet
    st.error("Feature encoders not found! Run train_attack_model.py first.")
    countries = sorted(df["country_txt"].dropna().unique())
    regions = sorted(df["region_txt"].dropna().unique())
    attacks = sorted(df["attacktype1_txt"].dropna().unique())
    weapons = sorted(df["weaptype1_txt"].dropna().unique())
    targets = sorted(df["targtype1_txt"].dropna().unique())

# ---------------------------------------------------
# 3. SIDEBAR: Display Clean Human Text Options
# ---------------------------------------------------
st.sidebar.header("Input Parameters")

selected_country = st.sidebar.selectbox("Country", countries)
selected_region = st.sidebar.selectbox("Region", regions)
selected_attack = st.sidebar.selectbox("Attack Type", attacks)
selected_weapon = st.sidebar.selectbox("Weapon Type", weapons)
selected_target = st.sidebar.selectbox("Target Type", targets)

# ---------------------------------------------------
# 4. TRANSLATION: Convert text choices back to model numbers
# ---------------------------------------------------
if os.path.exists(encoders_path):
    encoded_country = encoders["country_txt"].transform([selected_country])[0]
    encoded_region = encoders["region_txt"].transform([selected_region])[0]
    encoded_attack = encoders["attacktype1_txt"].transform([selected_attack])[0]
    encoded_weapon = encoders["weaptype1_txt"].transform([selected_weapon])[0]
    encoded_target = encoders["targtype1_txt"].transform([selected_target])[0]
else:
    encoded_country, encoded_region, encoded_attack, encoded_weapon, encoded_target = 0, 0, 0, 0, 0

# Visual breakdown check for you to see the mapped reference numbers
st.write("### Reference Mapping Codes (Sent to Model)")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(selected_country, f"Code: {encoded_country}")
col2.metric(selected_region, f"Code: {encoded_region}")
col3.metric(selected_attack, f"Code: {encoded_attack}")
col4.metric(selected_weapon, f"Code: {encoded_weapon}")
col5.metric(selected_target, f"Code: {encoded_target}")

# ---------------------------------------------------
# 5. PREDICTION BUTTON
# ---------------------------------------------------
if st.button("🚨 Predict Threat Level"):
    st.info("Ready to connect prediction logic here using encoded numbers!")
