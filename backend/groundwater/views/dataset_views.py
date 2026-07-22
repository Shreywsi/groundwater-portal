import os
import shutil

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ..models import Dataset

import logging

logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    from ml.preprocess import preprocess_dataset
    from ml.build_dataset import build_master_dataset
    from ml.dataset import set_active_dataset
    from ml.retrain import retrain_model
    file = request.FILES.get("file")

    if not file:
        return Response(
            {"success": False, "message": "No file uploaded"},
            status=400
        )

    upload_dir = os.path.join(settings.BASE_DIR, "uploads", "datasets", "active")
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.name)

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


    from ml.validate import validate_dataset

    validation = validate_dataset(file_path)

    if not validation["valid"]:
        return Response(
            validation,
            status=400
        )   
    active_dataset = set_active_dataset(file_path)
    from ml.retrain import retrain_model

    validation["active_dataset"] = active_dataset

    try:
        df = preprocess_dataset(active_dataset)
        # ---------------------------------------
        # Save processed dataset as active dataset
        # ---------------------------------------

        active_dataset = os.path.join(
            settings.BASE_DIR,
            "ml",
            "data",
            "processed",
            "database_training_data.csv"
        )

        df.to_csv(
            active_dataset,
            index=False
        )
    

    except Exception as e:
        os.remove(file_path)

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=400
        )
    archive_dir = os.path.join(
        settings.BASE_DIR,
        "uploads",
        "datasets",
        "archive"
    )

    os.makedirs(
        archive_dir,
        exist_ok=True
    )

    archive_path = os.path.join(
        archive_dir,
        file.name
    )

    import shutil

    shutil.copy(
        file_path,
        archive_path
    )

    total_rows = build_master_dataset()

    dataset = Dataset.objects.create(
        name=file.name,
        file_name=file.name,
        file_path=file_path,
        rows=total_rows,
        columns=len(df.columns),
    )


    return Response({

    "success": True,

    "message": "Dataset uploaded successfully.",

    "dataset": {

        "rows": validation["rows"],

        "columns": validation["columns"],

        "date_range": validation["date_range"],

        "missing_values": validation["missing_values"],

        "ready_for_training": True

    }

})