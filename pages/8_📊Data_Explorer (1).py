import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------
st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Terrorism Data Explorer")
st.markdown("Explore, filter, visualize, and extract records from the optimized GTD schema.")

# --------------------------------------------------------
# STYLED PUBLIC DATASET DISCLAIMER CAPTION
# --------------------------------------------------------
# This adds a distinct, high-visibility notification bar at the top of the app interface
st.markdown(
    """
    <div style="
        background-color: #ffe6e6; 
        border-left: 6px solid #ff3333; 
        padding: 12px; 
        border-radius: 4px; 
        margin-bottom: 20px;
    ">
        <strong style="color: #cc0000; font-size: 14px;">⚠️ Data Limitation Notice:</strong>
        <span style="color: #333333; font-size: 14px; font-weight: 500;">
            Although this tracking system contains historical data records stretching up to <strong>2017</strong>, 
            there may still be localized instances of incomplete or missing attributes since it relies entirely on a publicly available open dataset framework.
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)

# --------------------------------------------------------
# Load Dataset (HIGHLY OPTIMIZED 10-COLUMN FOOTPRINT)
# --------------------------------------------------------
@st.cache_data
def load_data():
    required_cols = [
        "iyear", "country_txt", "region_txt", "attacktype1_txt", 
        "weaptype1_txt", "gname", "city", "nkill", "nwound", "summary"
    ]
    df = pd.read_csv(
        "dataloader/globalterrorismdb_0718dist.csv",
        encoding="latin1",
        usecols=required_cols,
        low_memory=False
    )
    df["city"] = df["city"].fillna("Unknown")
    df["summary"] = df["summary"].fillna("No summary provided.")
    return df

df = load_data()

# --------------------------------------------------------
# Sidebar Filters
# --------------------------------------------------------
st.sidebar.header("Filter Dataset")

years = sorted(df["iyear"].dropna().unique())
selected_year = st.sidebar.multiselect("Select Year", years)

regions = sorted(df["region_txt"].dropna().unique())
selected_region = st.sidebar.multiselect("Select Region", regions)

if selected_region:
    countries_opts = sorted(df[df["region_txt"].isin(selected_region)]["country_txt"].unique())
else:
    countries_opts = sorted(df["country_txt"].dropna().unique())
selected_country = st.sidebar.multiselect("Select Country", countries_opts)

attack_types = sorted(df["attacktype1_txt"].dropna().unique())
selected_attack = st.sidebar.multiselect("Attack Type", attack_types)

weapons = sorted(df["weaptype1_txt"].dropna().unique())
selected_weapon = st.sidebar.multiselect("Weapon Type", weapons)

groups = sorted(df["gname"].dropna().unique())
selected_group = st.sidebar.multiselect("Terrorist Group", groups)

# --------------------------------------------------------
# Apply Filters
# --------------------------------------------------------
filtered_df = df.copy()

if selected_year:
    filtered_df = filtered_df[filtered_df["iyear"].isin(selected_year)]
if selected_region:
    filtered_df = filtered_df[filtered_df["region_txt"].isin(selected_region)]
if selected_country:
    filtered_df = filtered_df[filtered_df["country_txt"].isin(selected_country)]
if selected_attack:
    filtered_df = filtered_df[filtered_df["attacktype1_txt"].isin(selected_attack)]
if selected_weapon:
    filtered_df = filtered_df[filtered_df["weaptype1_txt"].isin(selected_weapon)]
if selected_group:
    filtered_df = filtered_df[filtered_df["gname"].isin(selected_group)]

# --------------------------------------------------------
# Search Box
# --------------------------------------------------------
search = st.text_input("🔍 Search Descriptions by City, Country, or Summary Details")
if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df["city"].str.lower().str.contains(search_lower, na=False) |
        filtered_df["country_txt"].str.lower().str.contains(search_lower, na=False) |
        filtered_df["summary"].str.lower().str.contains(search_lower, na=False)
    ]

if filtered_df.empty:
    st.error("⚠️ No entries match the current filter selection. Broaden your filters in the sidebar.")
    st.stop()

# --------------------------------------------------------
# KPIs
# --------------------------------------------------------
st.write("### Key Performance Indicators")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Incidents", f"{len(filtered_df):,}")
c2.metric("Active Countries", f"{filtered_df['country_txt'].nunique():,}")
c3.metric("Fatalities Recorded", f"{int(filtered_df['nkill'].fillna(0).sum()):,}")
c4.metric("Injuries Recorded", f"{int(filtered_df['nwound'].fillna(0).sum()):,}")

st.divider()

# --------------------------------------------------------
# Multi-Tab Layout Presentation
# --------------------------------------------------------
main_tab1, main_tab2, main_tab3 = st.tabs(["📋 Data Records Preview", "📈 Visual Analytics Dashboard", "⚙️ Data Integrity & Info"])

with main_tab1:
    st.subheader("Filtered Dataset Preview (Top 100 Rows)")
    
    st.dataframe(
        filtered_df.head(100),
        width="stretch",
        height=400
    )
    
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Filtered Dataset Extract (CSV)",
        csv_bytes,
        file_name="Filtered_GTD_Data.csv",
        mime="text/csv",
        width="stretch"
    )

with main_tab2:
    st.subheader("Core Incident Dimensions")
    chart_tab1, chart_tab2, chart_tab3 = st.tabs(["Geographic Vulnerability", "Methodology Breakdown", "Weapon Deployments"])
    
    with chart_tab1:
        country_chart = filtered_df["country_txt"].value_counts().head(10).reset_index()
        country_chart.columns = ["Country", "Incidents"]
        
        fig = px.bar(
            country_chart, x="Country", y="Incidents", color="Incidents",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            title="Top 10 High-Risk Nations Overview"
        )
        st.plotly_chart(fig, width="stretch")
        
    with chart_tab2:
        attack_chart = filtered_df["attacktype1_txt"].value_counts().reset_index()
        attack_chart.columns = ["Attack Type", "Count"]
        
        fig2 = px.pie(
            attack_chart, names="Attack Type", values="Count",
            color_discrete_sequence=px.colors.sequential.Reds_r,
            title="Operational Tactics Profile Distribution"
        )
        st.plotly_chart(fig2, width="stretch")
        
    with chart_tab3:
        weapon_chart = filtered_df["weaptype1_txt"].value_counts().head(10).reset_index()
        weapon_chart.columns = ["Weapon", "Count"]
        
        fig3 = px.bar(
            weapon_chart, x="Weapon", y="Count", color="Count",
            color_continuous_scale=px.colors.sequential.Oranges,
            title="Weapon Category Volume Trace"
        )
        st.plotly_chart(fig3, width="stretch")

with main_tab3:
    col_info_left, col_info_right = st.columns(2)
    
    with col_info_left:
        st.subheader("Completeness Evaluation Matrix")
        missing = filtered_df.isnull().sum().sort_values(ascending=False).reset_index()
        missing.columns = ["Data Attribute Feature", "Missing Cell Metrics"]
        
        st.dataframe(missing, width="stretch")
        
    with col_info_right:
        st.subheader("System Metadata Summary")
        st.info(f"""
        * **Active Subset Rows:** {filtered_df.shape[0]:,}
        * **Target Columns:** {filtered_df.shape[1]}
        * **Operational RAM Footprint:** {round(filtered_df.memory_usage(deep=True).sum()/1024**2,2)} MB
        """)
        
        st.write("**Tracked Active Attribute Vectors**")
        st.code(filtered_df.columns.tolist())
