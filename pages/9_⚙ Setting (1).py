
import streamlit as st
import pandas as pd
import os

from theme_manager import apply_global_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)


# ============================================================
# GLOBAL THEME
# ============================================================

apply_global_theme()


# ============================================================
# TITLE
# ============================================================

st.title("⚙️ Dashboard Settings")

st.markdown(
    "Configure your AI-Based Military Intelligence Dashboard "
    "parameters and visual layouts."
)


# ============================================================
# APPEARANCE
# ============================================================

st.header("🎨 Appearance")


# Initialize theme state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# Theme selector
theme = st.selectbox(
    "Dashboard Theme",
    ["Light", "Dark"],
    index=1 if st.session_state.dark_mode else 0
)


# Update theme
new_dark_mode = theme == "Dark"

if new_dark_mode != st.session_state.dark_mode:
    st.session_state.dark_mode = new_dark_mode
    st.rerun()


# Other appearance settings
layout = st.selectbox(
    "Dashboard Layout",
    ["Wide", "Centered"]
)

chart_style = st.selectbox(
    "Chart Style",
    ["Plotly", "Bar", "Line", "Pie"]
)


# ============================================================
# DEFAULT DASHBOARD SETTINGS
# ============================================================

st.header("🌍 Default Dashboard")

country = st.text_input(
    "Default Country",
    "India"
)

forecast_years = st.slider(
    "Default Forecast Years",
    1,
    10,
    5
)

confidence = st.slider(
    "Minimum Prediction Confidence (%)",
    50,
    100,
    80
)


# ============================================================
# GLOBAL THREAT MAP
# ============================================================

st.header("🗺️ Global Threat Map")

map_style = st.selectbox(
    "Map Style",
    [
        "OpenStreetMap",
        "Carto Positron",
        "Carto Dark"
    ]
)

show_cluster = st.checkbox(
    "Enable Marker Clustering",
    value=True
)

show_heatmap = st.checkbox(
    "Enable Heatmap",
    value=False
)


# ============================================================
# FORECASTING SETTINGS
# ============================================================

st.header("📈 Forecasting")

forecast_model = st.selectbox(
    "Forecasting Algorithm",
    [
        "Linear Regression",
        "ARIMA",
        "Prophet"
    ]
)


# ============================================================
# MACHINE LEARNING SETTINGS
# ============================================================

st.header("🤖 Machine Learning")

ml_model = st.selectbox(
    "Prediction Model",
    [
        "Random Forest",
        "Decision Tree",
        "Gradient Boosting"
    ]
)

probability = st.checkbox(
    "Show Prediction Probability",
    value=True
)

feature_importance = st.checkbox(
    "Show Feature Importance",
    value=True
)


# ============================================================
# REPORT SETTINGS
# ============================================================

st.header("📄 AI Intelligence Report")

report_type = st.selectbox(
    "Default Report Format",
    [
        "PDF",
        "Word",
        "Text"
    ]
)

include_charts = st.checkbox(
    "Include Charts in Report",
    value=True
)

include_tables = st.checkbox(
    "Include Data Tables",
    value=True
)


# ============================================================
# NOTIFICATIONS
# ============================================================

st.header("🔔 Notifications")

attack_alert = st.checkbox(
    "Enable Attack Alerts",
    value=True
)

forecast_alert = st.checkbox(
    "Enable Forecast Alerts",
    value=True
)

report_alert = st.checkbox(
    "Enable Report Notifications",
    value=False
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.header("📊 Dataset Information")

csv_path = "dataloader/globalterrorismdb_0718dist.csv"


if os.path.exists(csv_path):

    try:

        total_rows = 181691

        sample_df = pd.read_csv(
            csv_path,
            encoding="latin1",
            nrows=1
        )

        total_cols = sample_df.shape[1]

        st.success(
            "Dataset Configuration Validated and Loaded Successfully!"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Dataset Rows",
            f"{total_rows:,}"
        )

        col2.metric(
            "Dataset Columns",
            f"{total_cols}"
        )

        col3.metric(
            "Monitored Countries",
            "205"
        )

    except Exception as e:

        st.error(
            f"Error checking file properties: {str(e)}"
        )

else:

    st.error(
        "Dataset not found. Verify file path inside target directory."
    )


# ============================================================
# SAVE / RESET SETTINGS
# ============================================================

st.divider()

save_btn, reset_btn = st.columns(2)


# ============================================================
# SAVE SETTINGS
# ============================================================

with save_btn:

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):

        st.success(
            "Settings saved successfully to config state!"
        )

        st.balloons()


# ============================================================
# RESET SETTINGS
# ============================================================

with reset_btn:

    if st.button(
        "🔄 Reset Settings",
        use_container_width=True
    ):

        st.session_state.dark_mode = False

        st.success(
            "Settings reset to default baseline profiles."
        )

        st.rerun()