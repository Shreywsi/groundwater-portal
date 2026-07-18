import os
import joblib
import numpy as np
import pandas as pd
from ml.dataset import get_active_dataset

from tensorflow.keras.models import load_model

# Base directory of the ML module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "groundwater_model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "saved_models", "scaler.pkl")
DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "uploads",
    "datasets",
    "active",
    "training_data.csv"
)


def predict_groundwater():

    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = pd.read_csv(get_active_dataset())

    # Convert uploaded CSV format
    if "water_level_m" in df.columns:
        df["groundwater_depth"] = df["water_level_m"]

    if "water_balance" not in df.columns:
        df["water_balance"] = 0


    # Handle missing values
    df["rainfall_mm"] = df["rainfall_mm"].fillna(0)

    df["groundwater_depth"] = df["groundwater_depth"].fillna(
        df["groundwater_depth"].mean()
    )

    df["water_balance"] = df["water_balance"].fillna(0)


    features = [
        "rainfall_mm",
        "water_balance",
        "groundwater_depth"
    ]


    data = df[features].values


    scaled = scaler.transform(data)


    # Last 6 months sequence
    sequence = scaled[-6:]

    X = np.array([sequence])


    prediction_scaled = model.predict(
        X,
        verbose=0
    )


    # Convert prediction back
    predicted_depth_scaled = prediction_scaled[0][0]


    # Manual inverse scaling
    groundwater_min = scaler.data_min_[2]
    groundwater_max = scaler.data_max_[2]


    prediction = (
        predicted_depth_scaled *
        (groundwater_max - groundwater_min)
        + groundwater_min
    )


    return round(float(prediction), 2)


if __name__ == "__main__":
    prediction = predict_groundwater()
    print(f"Predicted Groundwater Depth: {prediction} meters")