import streamlit as st
import joblib
import pandas as pd
from theme_manager import apply_global_theme
from dataloader.data_loader import load_data

# Initialize model and encoders
model = joblib.load("models/incident_prediction_model.pkl")
encoders = joblib.load("models/feature_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

st.set_page_config(
    page_title="Incident Analysis",
    page_icon="📊",
    layout="wide"
)

apply_global_theme()

st.title("📊 Incident Type Prediction")

st.markdown("""
Enter the incident details below and click **Predict Incident Type**.
""")

df = load_data()

# Clean data for dropdown selection
df = df.dropna(subset=[
    "location_txt",
    "area_txt",
    "equipment_txt",
    "subject_txt",
    "organization_name"
])

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        location = st.selectbox(
            "🌍 Location",
            sorted(df["location_txt"].unique())
        )

        area = st.selectbox(
            "🌎 Area/Region",
            sorted(df["area_txt"].unique())
        )

        equipment = st.selectbox(
            "🛠 Equipment Involved",
            sorted(df["equipment_txt"].unique())
        )

        subject = st.selectbox(
            "🎯 Subject Type",
            sorted(df["subject_txt"].unique())
        )

    with col2:

        organization = st.selectbox(
            "👥 Organization",
            sorted(df["organization_name"].unique())
        )

        resolved = st.selectbox(
            "✅ Resolution Achieved?",
            [1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )

        severity = st.number_input(
            "⚠️ Severity Scale (0-10)",
            min_value=0,
            max_value=10,
            value=0,
            step=1
        )

        impact_count = st.number_input(
            "📈 Impact Metric",
            min_value=0,
            value=0,
            step=1
        )

    submitted = st.form_submit_button("🚀 Predict Incident Type")

if submitted:
    # Transform inputs using encoders
    loc_enc = encoders["location_txt"].transform([location])[0]
    area_enc = encoders["area_txt"].transform([area])[0]
    equip_enc = encoders["equipment_txt"].transform([equipment])[0]
    sub_enc = encoders["subject_txt"].transform([subject])[0]
    org_enc = encoders["organization_name"].transform([organization])[0]

    input_df = pd.DataFrame({
        "location_txt": [loc_enc],
        "area_txt": [area_enc],
        "equipment_txt": [equip_enc],
        "subject_txt": [sub_enc],
        "organization_name": [org_enc],
        "resolution": [resolved],
        "severity": [severity],
        "impact_metric": [impact_count]
    })
    
    prediction = model.predict(input_df)
    incident_type = target_encoder.inverse_transform(prediction)[0]
    st.success(f"Predicted Incident Type: {incident_type}")
    
    probabilities = model.predict_proba(input_df)
    confidence = probabilities.max() * 100

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

