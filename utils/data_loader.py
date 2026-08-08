import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Points to  compressed dataset
    return pd.read_parquet("dataloader/globalterrorismdb_small.parquet")
