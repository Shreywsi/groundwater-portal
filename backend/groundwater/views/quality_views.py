from datetime import datetime

from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ..models import TDS, Salinity

import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
def water_quality(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                q.time,
                w.well_name,
                q.tds_ppm,
                q.salinity_ppt
            FROM water_quality q
            JOIN wells w
            ON q.well_id = w.id
            ORDER BY q.time;
        """)

        columns = [col[0] for col in cursor.description]

        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return Response(rows)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_water_quality(request):
    """
    Expects JSON body: { "well_id": int, "time": "YYYY-MM-DD", "tds_ppm": float, "salinity_ppt": float }
    Either tds_ppm or salinity_ppt can be omitted (null), but at least one is required.
    """
    well_id = request.data.get("well_id")
    time = request.data.get("time")
    tds_ppm = request.data.get("tds_ppm")
    salinity_ppt = request.data.get("salinity_ppt")

    if well_id is None or not time:
        return Response({"error": "well_id and time are required."}, status=400)

    if tds_ppm is None and salinity_ppt is None:
        return Response({"error": "Provide at least one of tds_ppm or salinity_ppt."}, status=400)

    try:
        datetime.strptime(time, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "time must be in YYYY-MM-DD format."}, status=400)

    try:
        tds_ppm = float(tds_ppm) if tds_ppm is not None else None
        salinity_ppt = float(salinity_ppt) if salinity_ppt is not None else None
    except (TypeError, ValueError):
        return Response({"error": "tds_ppm and salinity_ppt must be numbers."}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM wells WHERE id = %s;", [well_id])
            if cursor.fetchone() is None:
                return Response({"error": "Well not found."}, status=404)

            cursor.execute("""
                INSERT INTO water_quality (well_id, time, tds_ppm, salinity_ppt)
                VALUES (%s, %s, %s, %s);
            """, [well_id, time, tds_ppm, salinity_ppt])
    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response({"error": str(e)}, status=500)

    return Response({
        "success": True, "well_id": well_id, "time": time,
        "tds_ppm": tds_ppm, "salinity_ppt": salinity_ppt
    }, status=201)


@api_view(["GET"])
def tds(request):
    data = [
        {"date": t.date, "value": t.value}
        for t in TDS.objects.all().order_by("date")
    ]
    return Response(data)


@api_view(["GET"])
def salinity(request):
    data = [
        {"date": s.date, "value": s.value}
        for s in Salinity.objects.all().order_by("date")
    ]
    return Response(data)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_tds(request):
    """Expects JSON body: { "date": "YYYY-MM-DD", "value": float }"""
    date = request.data.get("date")
    value = request.data.get("value")

    if not date or value is None:
        return Response({"error": "date and value are required."}, status=400)

    try:
        datetime.strptime(date, "%Y-%m-%d")
        value = float(value)
    except (ValueError, TypeError):
        return Response({"error": "Invalid date or value."}, status=400)

    entry = TDS.objects.create(date=date, value=value)
    return Response({"success": True, "id": entry.id, "date": date, "value": value}, status=201)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_salinity(request):
    """Expects JSON body: { "date": "YYYY-MM-DD", "value": float }"""
    date = request.data.get("date")
    value = request.data.get("value")

    if not date or value is None:
        return Response({"error": "date and value are required."}, status=400)

    try:
        datetime.strptime(date, "%Y-%m-%d")
        value = float(value)
    except (ValueError, TypeError):
        return Response({"error": "Invalid date or value."}, status=400)

    entry = Salinity.objects.create(date=date, value=value)
    return Response({"success": True, "id": entry.id, "date": date, "value": value}, status=201)