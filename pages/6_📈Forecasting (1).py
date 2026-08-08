import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Advanced Terrorism Attack Forecasting")

st.markdown("""
Dynamically filter the dataset using the sidebar parameters to generate a custom trend forecast.
""")

# ----------------------------------------------------
# Load Dataset (OPTIMIZED & EXPANDED TO 8 SAFE COLUMNS)
# ----------------------------------------------------
@st.cache_data
def load_data():
    # Strict 8-column schema prevents server RAM memory exhaustion crashes
    required_cols = [
        "country_txt", 
        "iyear", 
        "nkill", 
        "nwound", 
        "gname", 
        "attacktype1_txt", 
        "weaptype1_txt",
        "targtype1_txt"
    ]
    df = pd.read_csv(
        "dataloader/globalterrorismdb_0718dist.csv",
        encoding="latin1",
        usecols=required_cols,
        low_memory=False
    )
    return df

df = load_data()

# ----------------------------------------------------
# Sidebar: Dynamic Filter Selector
# ----------------------------------------------------
st.sidebar.header("Filter Settings")

# 1. Primary Filter Required for Linear Forecasting
countries = sorted(df["country_txt"].dropna().unique())
country = st.sidebar.selectbox("Base Country Focus", countries)

# Filter the primary working dataframe by country first
filtered_df = df[df["country_txt"] == country]

# 2. Dynamic Column Filter Selection
st.sidebar.subheader("Add Additional Filters")
available_filters = {
    "gname": "Terrorist Group",
    "attacktype1_txt": "Attack Type",
    "weaptype1_txt": "Weapon Type",
    "targtype1_txt": "Target Type"
}

chosen_filters = st.sidebar.multiselect(
    "Choose criteria to narrow down data:",
    options=list(available_filters.keys()),
    format_func=lambda x: available_filters[x]
)

# 3. Render Chosen Filters Dynamically
for col_name in chosen_filters:
    unique_options = sorted(filtered_df[col_name].dropna().unique())
    selected_vals = st.sidebar.multiselect(
        f"Select {available_filters[col_name]} Options",
        options=unique_options,
        default=unique_options[:2] if len(unique_options) > 1 else unique_options
    )
    if selected_vals:
        filtered_df = filtered_df[filtered_df[col_name].isin(selected_vals)]

# 4. Forecast Span Settings Slider
forecast_years = st.sidebar.slider(
    "Forecast Projection Horizon (Years)",
    1, 10, 5
)

# ----------------------------------------------------
# Prepare Regression Modeling Data Series
# ----------------------------------------------------
yearly = (
    filtered_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)
yearly = yearly.sort_values("iyear")

# ----------------------------------------------------
# Guard Rails: Check Data Density
# ----------------------------------------------------
if len(yearly) < 3:
    st.error("❌ **Insufficient Data Point Density:** The applied filter combination leaves too few historical data points to fit a linear regression line. Broaden your sidebar criteria.")
    st.stop()

# ----------------------------------------------------
# Train Linear Regression Model
# ----------------------------------------------------
X = yearly[["iyear"]]
y = yearly["Attacks"]

model = LinearRegression()
model.fit(X, y)

# ----------------------------------------------------
# Future Prediction Calculations
# ----------------------------------------------------
last_year = int(yearly["iyear"].max())

future_years = np.arange(
    last_year + 1,
    last_year + forecast_years + 1
)

future_df = pd.DataFrame({
    "iyear": future_years
})

predictions = model.predict(future_df)
predictions = np.maximum(predictions, 0)  # Attacks cannot fall below zero

forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": predictions.astype(int)
})

# ----------------------------------------------------
# Display Historical + Forecast Visual Chart Trace
# ----------------------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical Records"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Predictive Trend"
    )
)

fig.update_layout(
    title=f"Custom Filtered Attack Forecast for {country}",
    xaxis_title="Year",
    yaxis_title="Number of Incidents",
    height=500
)

# Render full width using future-proof syntax parameters
st.plotly_chart(fig, width="stretch")

# ----------------------------------------------------
# Metrics & Growth Analysis Display Interface
# ----------------------------------------------------
st.subheader("Data Insights & Metrics")

historical_last = float(yearly.iloc[-1]["Attacks"]) if not yearly.empty else 0.0
forecast_last = float(forecast.iloc[-1]["Forecasted Attacks"]) if not forecast.empty else 0.0

denom = max(historical_last, 1.0)
growth = ((forecast_last - historical_last) / denom) * 100.0

col1, col2, col3 = st.columns(3)
col1.metric("Latest Historical Incidents", int(historical_last))
col2.metric(f"Forecasted Incidents ({forecast_years} Years Out)", int(forecast_last))
col3.metric("Projected Shift %", f"{growth:.2f}%")

# Trend Evaluation
if growth < 0:
    st.success("🟢 Security Outlook Profile: Trend Declining")
elif growth < 15:
    st.warning("🟡 Security Outlook Profile: Stable Baseline")
else:
    st.error("🔴 Security Outlook Profile: Threat Vector Escalating")

# ----------------------------------------------------
# Forecast Table & Data Extraction Port
# ----------------------------------------------------
st.subheader("Forecast Target Breakdown")

st.dataframe(
    forecast,
    width="stretch"
)

# Export Functionality Engine mapping
csv_bytes = forecast.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Export Forecast Dataset (CSV)",
    data=csv_bytes,
    file_name=f"{country}_custom_forecast.csv",
    mime="text/csv",
    width="stretch"
)
