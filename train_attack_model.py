import numpy as np
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# ---------------------------------------------------
# Create models folder
# ---------------------------------------------------
os.makedirs("models", exist_ok=True)
# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
print("Loading GTD Dataset...")
df = pd.read_csv(
    "dataloader/globalterrorismdb_small.parquet",
    encoding="latin1",
    low_memory=False
)
print(df.shape)
# ---------------------------------------------------
# Select Features
# ---------------------------------------------------
features = [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname",
    "success",
    "suicide",
    "nkill",
    "nwound"
]
target = "attacktype1_txt"
df = df[features + [target]]
# ---------------------------------------------------
# Remove Missing Values
# ---------------------------------------------------
df = df.dropna()
print("After Cleaning:", df.shape)
# ---------------------------------------------------
# Encode Features
# ---------------------------------------------------
encoders = {}
for col in [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname"
]:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])
    encoders[col] = encoder