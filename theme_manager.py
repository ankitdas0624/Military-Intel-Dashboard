# Save this file as: theme_manager.py
import streamlit as st

def apply_global_theme():
    # Initialize the global state tracker if it doesn't exist yet
    if "current_theme" not in st.session_state:
        st.session_state.current_theme = "Light"

    # Inject dark CSS dynamically if the user toggled Dark Mode on the settings page
    if st.session_state.current_theme == "Dark":
        st.markdown(
            """
            <style>
            /* Global main app canvas and sidebar background override */
            .stApp, [data-testid="stSidebar"], [data-testid="stHeader"] {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            /* Universal text alignment and text coloring rules */
            h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
                color: #ffffff !important;
            }
            /* Styling form components, selectboxes, dataframes, and sliders */
            div[data-baseweb="select"], input, textarea, .stSlider, .stDataFrame, div[role="listbox"] {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            /* Dynamic page element borders and layout dividers */
            hr {
                border-color: #444444 !important;
            }
            div[data-testid="stMetricBorder"] {
                border-color: #2d2d2d !important;
                background-color: #262626 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
