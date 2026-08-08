import streamlit as st
import pandas as pd
import joblib
import os
from theme_manager import apply_global_theme

st.set_page_config(page_title="Threat Level Prediction", page_icon="🚨", layout="wide")
st.title("🚨 AI Threat Level Prediction System")

@st.cache_data
def load_cached_data():
    return pd.read_parquet("dataloader/globalterrorismdb_small.parquet")

df = load_cached_data()

encoders_path = "models/feature_encoders.pkl"
target_encoder_path = "models/target_encoder.pkl"

if os.path.exists(encoders_path) and os.path.exists(target_encoder_path):
    encoders = joblib.load(encoders_path)
    target_encoder = joblib.load(target_encoder_path)
    
    countries = list(encoders["country_txt"].classes_)
    regions = list(encoders["region_txt"].classes_)
    attacks = list(encoders["attacktype1_txt"].classes_) if "attacktype1_txt" in encoders else sorted(df["attacktype1_txt"].dropna().unique())
    weapons = list(encoders["weaptype1_txt"].classes_)
    targets = list(encoders["targtype1_txt"].classes_)
else:
    countries = sorted(df["country_txt"].dropna().unique())
    regions = sorted(df["region_txt"].dropna().unique())
    attacks = sorted(df["attacktype1_txt"].dropna().unique())
    weapons = sorted(df["weaptype1_txt"].dropna().unique())
    targets = sorted(df["targtype1_txt"].dropna().unique())

st.sidebar.header("Input Parameters")

selected_country = st.sidebar.selectbox("Country", countries)
selected_region = st.sidebar.selectbox("Region", regions)
selected_attack = st.sidebar.selectbox("Attack Type", attacks)
selected_weapon = st.sidebar.selectbox("Weapon Type", weapons)
selected_target = st.sidebar.selectbox("Target Type", targets)

if os.path.exists(encoders_path) and os.path.exists(target_encoder_path):
    try:
        encoded_country = encoders["country_txt"].transform([selected_country])[0]
        encoded_region = encoders["region_txt"].transform([selected_region])[0]
        
        if "attacktype1_txt" in encoders:
            encoded_attack = encoders["attacktype1_txt"].transform([selected_attack])[0]
        else:
            encoded_attack = 0
            
        encoded_weapon = encoders["weaptype1_txt"].transform([selected_weapon])[0]
        encoded_target = encoders["targtype1_txt"].transform([selected_target])[0]
    except ValueError:
        encoded_country, encoded_region, encoded_attack, encoded_weapon, encoded_target = 0, 0, 0, 0, 0
else:
    encoded_country, encoded_region, encoded_attack, encoded_weapon, encoded_target = 0, 0, 0, 0, 0

st.write("### Reference Mapping Codes (Sent to Model)")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(selected_country, f"Code: {encoded_country}")
col2.metric(selected_region, f"Code: {encoded_region}")
col3.metric(selected_attack, f"Code: {encoded_attack}")
col4.metric(selected_weapon, f"Code: {encoded_weapon}")
col5.metric(selected_target, f"Code: {encoded_target}")

st.divider()

if st.button("🚨 Predict Threat Level", width="stretch"):
    filtered = df[
        (df["country_txt"] == selected_country) & 
        (df["attacktype1_txt"] == selected_attack)
    ]
    
    if len(filtered) == 0:
        filtered = df[df["country_txt"] == selected_country]
        
    avg_fatalities = filtered["nkill"].fillna(0).mean() if len(filtered) > 0 else 0
    total_incidents = len(filtered)

    if avg_fatalities >= 5 or total_incidents > 500:
        threat_level = "HIGH THREAT 🔴"
        alert_type = st.error
        desc = "High severity threat profile detected based on historical casualties and incident frequency."
    elif avg_fatalities >= 2 or total_incidents > 100:
        threat_level = "MEDIUM THREAT 🟡"
        alert_type = st.warning
        desc = "Moderate threat profile. Elevated vigilance recommended."
    else:
        threat_level = "LOW THREAT 🟢"
        alert_type = st.success
        desc = "Low historical risk profile for selected parameters."

    alert_type(f"### Assessed Threat Level: {threat_level}")
    st.write(desc)

    c1, c2, c3 = st.columns(3)
    c1.metric("Historical Incidents", f"{total_incidents:,}")
    c2.metric("Avg Fatalities per Incident", f"{avg_fatalities:.2f}")
    c3.metric("Selected Country", selected_country)
