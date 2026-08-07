import numpy as np
import os
import joblib
import pandas as pd
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
    "dataloader/globalterrorismdb_0718dist.csv",
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

# ---------------------------------------------------
# Encode Target Variable (Added to fix target_encoder.pkl)
# ---------------------------------------------------
target_encoder = LabelEncoder()
df[target] = target_encoder.fit_transform(df[target])

# ---------------------------------------------------
# Split Data into Train and Test Sets
# ---------------------------------------------------
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------------
# Train the Model
# ---------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ---------------------------------------------------
# Evaluate the Model
# ---------------------------------------------------
y_pred = model.predict(X_test)

print("\n", classification_report(y_test, y_pred))

print("====================================================")
print("Confusion Matrix")
print("====================================================")
print(confusion_matrix(y_test, y_pred))

# ---------------------------------------------------
# Save the Trained Model and Encoders (Updated Section)
# ---------------------------------------------------
# 1. Save the main machine learning model
joblib.dump(model, "models/attack_prediction_model.pkl")

# 2. Save the dictionary of feature encoders
joblib.dump(encoders, "models/feature_encoders.pkl")

# 3. Save the separate target encoder
joblib.dump(target_encoder, "models/target_encoder.pkl")

print("\n====================================================")
print("Model Saved Successfully")
print("====================================================")
