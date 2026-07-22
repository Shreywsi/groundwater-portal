import os
import json
from datetime import datetime

import pandas as pd

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ml.predict import predict_water_balance
from ..gempy_service import build_geological_model
from ..modflow_service import run_modflow
from ..models import Dataset, Location, WaterBalance

import logging

logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def run_gempy(request):
    result = build_geological_model()
    return Response(result)


@api_view(["POST"])
def run_modflow_view(request):

    # Step 1: Build geology
    geology = build_geological_model()

    # Step 2: Run groundwater model
    modflow = run_modflow()

    return Response({
        "success": True,
        "gempy": geology,
        "modflow": modflow
    })


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def retrain_lstm(request):
    from ml.retrain import retrain_model
    location_id = request.data.get("location")

    if not location_id:

        return Response(
            {
                "success": False,
                "message": "Location required."
            },
            status=400
        )

    result = retrain_model(location_id)

    if result["success"]:
        return Response(result)

    return Response(result, status=500)


@api_view(["GET"])
def ai_dashboard(request):


    location_id = request.GET.get("location")

    if not location_id:
        return Response({
            "success": False,
            "message": "Location is required."
        }, status=400)

    master_dataset = os.path.join(
        settings.BASE_DIR,
        "ml",
        "data",
        "processed",
        "database_training_data.csv"
    )

    rows = 0

    if os.path.exists(master_dataset):
        df = pd.read_csv(master_dataset)
        rows = len(df)

    model_dir = os.path.join(
        settings.BASE_DIR,
        "ml",
        "saved_models",
        f"location_{location_id}",
    )

    model_path = os.path.join(model_dir, "water_balance_model.keras")
    scaler_path = os.path.join(model_dir, "water_balance_scaler.pkl")

    model_ready = (
        os.path.exists(model_path)
        and
        os.path.exists(scaler_path)
    )

    prediction = None

    if model_ready:
        try:
            prediction = predict_water_balance(int(location_id))
        except Exception:
            prediction = None

    metrics = {}
    metrics_path = os.path.join(model_dir, "model_metrics.json")

    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    rmse = metrics.get("water_balance", {}).get("rmse")
    mae = metrics.get("water_balance", {}).get("mae")
    r2 = metrics.get("water_balance", {}).get("r2")

    train_samples = metrics.get("train_samples")
    test_samples = metrics.get("test_samples")

    confidence = None

    if r2 is not None:
        confidence = round(max(0, min(r2 * 100, 100)), 1)

    forecast_min = None
    forecast_max = None

    if prediction is not None and rmse is not None:
        forecast_min = round(prediction - rmse, 2)
        forecast_max = round(prediction + rmse, 2)

    last_training = None

    if model_ready:
        last_training = datetime.fromtimestamp(
            os.path.getmtime(model_path)
        ).strftime("%d %b %Y %H:%M")

    dataset_count = Dataset.objects.count()

    return Response({
        "summary": {
            "training_rows": rows,
            "dataset_count": dataset_count,
            "model_ready": model_ready,
            "last_training": last_training,
            "prediction": prediction,
            "confidence": confidence,
            "forecast_min": forecast_min,
            "forecast_max": forecast_max,
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
            "train_samples": train_samples,
            "test_samples": test_samples,
        }
    })


@api_view(["GET"])

def forecast_api(request, period):
    periods = {
        "monthly": 1,
        "quarterly": 3,
        "halfyearly": 6,
        "annual": 12,
        "10years": 120,
        "30years": 360,
    }

    if period not in periods:
        return Response(
            {
                "success": False,
                "message": "Invalid forecast period."
            },
            status=400
        )

    location_id = request.GET.get("location")

    if not location_id:
        return Response(
            {
                "success": False,
                "message": "Location is required."
            },
            status=400
        )

    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Invalid location."
            },
            status=400
        )

    steps = periods[period]

    try:
        forecast = predict_water_balance(
            location.id,
            steps
        )

        prediction = forecast[-1]
    except Exception as e:
        logger.exception("Prediction failed")

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=500
        )
    metrics_path = os.path.join(
    settings.BASE_DIR,
    "ml",
    "saved_models",
    f"location_{location.id}",
    "model_metrics.json",
)

    metrics = {}

    if os.path.exists(metrics_path):
        with open(metrics_path) as f:
            metrics = json.load(f)

    record_count = WaterBalance.objects.filter(
        location=location
    ).count()

    rmse = metrics.get("water_balance", {}).get("rmse")
    mae = metrics.get("water_balance", {}).get("mae")
    r2 = metrics.get("water_balance", {}).get("r2")

    # -------------------------
    # Confidence
    # -------------------------

    if r2 is None:
        confidence = 0
    else:
        confidence = round(max(0, min(r2 * 100, 100)), 1)

    # -------------------------
    # Confidence Level
    # -------------------------

    if confidence >= 90:
        confidence_level = "Very High"

    elif confidence >= 75:
        confidence_level = "High"

    elif confidence >= 50:
        confidence_level = "Medium"

    else:
        confidence_level = "Low"

    # -------------------------
    # Prediction Range
    # -------------------------

    if rmse is None:

        lower = prediction

        upper = prediction

    else:

        lower = round(prediction - rmse, 2)

        upper = round(prediction + rmse, 2)

    result = {

    "prediction": prediction,

    "forecast": forecast,
        "confidence": confidence,

        "confidence_level": confidence_level,

        "prediction_range": {

            "lower": lower,

            "upper": upper,

        },

        "years_of_history": record_count,

        "model_metrics": metrics,

    }

    return Response({
        "success": True,
        "location": location.name,
        "period": period,
        "steps": steps,
        **result
    })