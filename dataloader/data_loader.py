import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Update the string below if your new file has a slightly different name
    file_path = "dataloader/globalterrorismdb_0718dist.csv"
    
    # Read the full dataset with proper encoding for international text characters
    df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
    
    # Clean core structural columns to prevent math calculation errors
    df = df.dropna(subset=["iyear"])
    df["iyear"] = df["iyear"].astype(int)
    
    # Fill missing casualty or injury rows with 0 instead of leaving them empty (NaN)
    df["nkill"] = pd.to_numeric(df["nkill"], errors='coerce').fillna(0).astype(int)
    df["nwound"] = pd.to_numeric(df["nwound"], errors='coerce').fillna(0).astype(int)
    
    return df
