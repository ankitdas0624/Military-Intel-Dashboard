import streamlit as st


def apply_global_theme():

    # Default theme
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if st.session_state.dark_mode:

        background = "#0E1117"
        secondary = "#161B22"
        text = "#FFFFFF"
        border = "#30363D"
        input_bg = "#21262D"

    else:

        background = "#FFFFFF"
        secondary = "#F5F7FA"
        text = "#111827"
        border = "#D1D5DB"
        input_bg = "#FFFFFF"

    st.markdown(
        f"""
        <style>

        /* Main application */
        .stApp {{
            background-color: {background};
            color: {text};
        }}

        /* Main content */
        .main {{
            background-color: {background};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {secondary};
        }}

        section[data-testid="stSidebar"] * {{
            color: {text} !important;
        }}

        /* Headings and normal text */
        h1, h2, h3, h4, h5, h6, p, label {{
            color: {text} !important;
        }}

        /* Select boxes */
        div[data-baseweb="select"] > div {{
            background-color: {input_bg};
            border-color: {border};
        }}

        div[data-baseweb="select"] * {{
            color: {text} !important;
        }}

        /* Text inputs */
        div[data-baseweb="input"] > div {{
            background-color: {input_bg};
            border-color: {border};
        }}

        input {{
            color: {text} !important;
        }}

        /* Containers / cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: {border};
        }}

        </style>
        """,
        unsafe_allow_html=True
    )