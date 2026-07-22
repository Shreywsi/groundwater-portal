from datetime import datetime

from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from ..models import WaterTable

import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
def waterlevel(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                g.time,
                w.well_name,
                g.water_level_m
            FROM groundwater_levels g
            JOIN wells w
            ON g.well_id = w.id
            ORDER BY g.time;
        """)

        columns = [col[0] for col in cursor.description]

        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return Response(rows)


@api_view(["GET"])
def pumping(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                p.time,
                w.well_name,
                p.pumping_hours
            FROM pumping p
            JOIN wells w
            ON p.well_id = w.id
            ORDER BY p.time;
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
def add_water_level(request):
    """
    Admin endpoint to add a new groundwater level reading for a well.
    Expects JSON body: { "well_id": int, "time": "YYYY-MM-DD", "water_level_m": float }
    """
    well_id = request.data.get("well_id")
    time = request.data.get("time")
    water_level_m = request.data.get("water_level_m")

    if well_id is None or not time or water_level_m is None:
        return Response(
            {"error": "well_id, time, and water_level_m are all required."},
            status=400
        )

    try:
        datetime.strptime(time, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "time must be in YYYY-MM-DD format."}, status=400)

    try:
        water_level_m = float(water_level_m)
    except (TypeError, ValueError):
        return Response({"error": "water_level_m must be a number."}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM wells WHERE id = %s;", [well_id])
            if cursor.fetchone() is None:
                return Response({"error": "Well not found."}, status=404)

            cursor.execute("""
                INSERT INTO groundwater_levels (well_id, time, water_level_m)
                VALUES (%s, %s, %s);
            """, [well_id, time, water_level_m])
    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response({"error": str(e)}, status=500)

    return Response({
        "success": True,
        "well_id": well_id,
        "time": time,
        "water_level_m": water_level_m
    }, status=201)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_pumping(request):
    """
    Expects JSON body: { "well_id": int, "time": "YYYY-MM-DD", "pumping_hours": float }
    """
    well_id = request.data.get("well_id")
    time = request.data.get("time")
    pumping_hours = request.data.get("pumping_hours")

    if well_id is None or not time or pumping_hours is None:
        return Response(
            {"error": "well_id, time, and pumping_hours are all required."},
            status=400
        )

    try:
        datetime.strptime(time, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "time must be in YYYY-MM-DD format."}, status=400)

    try:
        pumping_hours = float(pumping_hours)
    except (TypeError, ValueError):
        return Response({"error": "pumping_hours must be a number."}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM wells WHERE id = %s;", [well_id])
            if cursor.fetchone() is None:
                return Response({"error": "Well not found."}, status=404)

            cursor.execute("""
                INSERT INTO pumping (well_id, time, pumping_hours)
                VALUES (%s, %s, %s);
            """, [well_id, time, pumping_hours])
    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response({"error": str(e)}, status=500)

    return Response({
        "success": True, "well_id": well_id, "time": time, "pumping_hours": pumping_hours
    }, status=201)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_rainfall(request):
    """
    Expects JSON body: { "station_name": str, "time": "YYYY-MM-DD", "rainfall_mm": float }
    """
    station_name = request.data.get("station_name")
    time = request.data.get("time")
    rainfall_mm = request.data.get("rainfall_mm")

    if not station_name or not time or rainfall_mm is None:
        return Response(
            {"error": "station_name, time, and rainfall_mm are all required."},
            status=400
        )

    try:
        datetime.strptime(time, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "time must be in YYYY-MM-DD format."}, status=400)

    try:
        rainfall_mm = float(rainfall_mm)
    except (TypeError, ValueError):
        return Response({"error": "rainfall_mm must be a number."}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO rainfall (time, station_name, rainfall_mm)
                VALUES (%s, %s, %s);
            """, [time, station_name, rainfall_mm])
    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response({"error": str(e)}, status=500)

    return Response({
        "success": True, "station_name": station_name, "time": time, "rainfall_mm": rainfall_mm
    }, status=201)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_weather(request):
    """
    Expects JSON body: { "station_name": str, "time": "YYYY-MM-DD", "temperature_c": float, "humidity_pct": float }
    """
    station_name = request.data.get("station_name")
    time = request.data.get("time")
    temperature_c = request.data.get("temperature_c")
    humidity_pct = request.data.get("humidity_pct")

    if not station_name or not time or temperature_c is None or humidity_pct is None:
        return Response(
            {"error": "station_name, time, temperature_c, and humidity_pct are all required."},
            status=400
        )

    try:
        datetime.strptime(time, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "time must be in YYYY-MM-DD format."}, status=400)

    try:
        temperature_c = float(temperature_c)
        humidity_pct = float(humidity_pct)
    except (TypeError, ValueError):
        return Response({"error": "temperature_c and humidity_pct must be numbers."}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO weather (time, station_name, temperature_c, humidity_pct)
                VALUES (%s, %s, %s, %s);
            """, [time, station_name, temperature_c, humidity_pct])
    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response({"error": str(e)}, status=500)

    return Response({
        "success": True, "station_name": station_name, "time": time,
        "temperature_c": temperature_c, "humidity_pct": humidity_pct
    }, status=201)


@api_view(["GET"])
def watertable(request):
    data = [
        {"date": w.date, "depth": w.depth}
        for w in WaterTable.objects.all().order_by("date")
    ]
    return Response(data)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_watertable(request):
    """Expects JSON body: { "date": "YYYY-MM-DD", "depth": float }"""
    date = request.data.get("date")
    depth = request.data.get("depth")

    if not date or depth is None:
        return Response({"error": "date and depth are required."}, status=400)

    try:
        datetime.strptime(date, "%Y-%m-%d")
        depth = float(depth)
    except (ValueError, TypeError):
        return Response({"error": "Invalid date or depth."}, status=400)

    entry = WaterTable.objects.create(date=date, depth=depth)
    return Response({"success": True, "id": entry.id, "date": date, "depth": depth}, status=201)