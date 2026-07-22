from django.db import connection

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
def dashboard(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT COUNT(*) FROM wells;
        """)
        total_wells = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT village) FROM wells;
        """)
        total_villages = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM groundwater_levels;
        """)
        groundwater_records = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM pumping;
        """)
        pumping_records = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM rainfall;
        """)
        rainfall_records = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM weather;
        """)
        weather_records = cursor.fetchone()[0]

    return Response({
        "totalWells": total_wells,
        "totalVillages": total_villages,
        "totalRecords": groundwater_records + pumping_records + rainfall_records + weather_records,
        "groundwaterRecords": groundwater_records,
        "pumpingRecords": pumping_records,
        "rainfallRecords": rainfall_records,
        "weatherRecords": weather_records
    })


@api_view(["GET"])
def wells(request):

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                id,
                well_name,
                village,
                latitude,
                longitude,
                depth_m,
                water_level_m,
                status
            FROM groundwater_map
            ORDER BY id;
        """)

        columns = [col[0] for col in cursor.description]

        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return Response(rows)


@api_view(["GET"])
def village_clusters_geojson(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(
                    ST_AsGeoJSON(t.*)::json
                )
            )
            FROM (
                SELECT
                    ogc_fid,
                    wkb_geometry
                FROM village_clusters
            ) AS t;
        """)

        geojson = cursor.fetchone()[0]

    return Response(geojson)


# views.py — well property box endpoint

@api_view(["GET"])
def well_detail(request, well_id):
    try:
        with connection.cursor() as cursor:

            # ------------------------
            # Well information
            # ------------------------
            cursor.execute("""
                SELECT
                    id,
                    well_name,
                    village,
                    latitude,
                    longitude,
                    depth_m,
                    water_level_m,
                    status
                FROM groundwater_map
                WHERE id = %s;
            """, [well_id])

            row = cursor.fetchone()

            if not row:
                return Response(
                    {"error": "Well not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            columns = [col[0] for col in cursor.description]
            well = dict(zip(columns, row))

            # ------------------------
            # Monthly history
            # ------------------------
            cursor.execute("""
                SELECT
                    date_trunc('month', time) AS period,
                    AVG(water_level_m) AS avg_level
                FROM groundwater_levels
                WHERE well_id = %s
                GROUP BY period
                ORDER BY period;
            """, [well_id])

            monthly = []

            for period, level in cursor.fetchall():
                if period and level is not None:
                    monthly.append({
                        "period": period.strftime("%Y-%m"),
                        "level": round(level, 2)
                    })

            # ------------------------
            # Quarterly history
            # ------------------------
            cursor.execute("""
                SELECT
                    date_trunc('quarter', time) AS period,
                    AVG(water_level_m) AS avg_level
                FROM groundwater_levels
                WHERE well_id = %s
                GROUP BY period
                ORDER BY period;
            """, [well_id])

            quarterly = []

            for period, level in cursor.fetchall():
                if period and level is not None:
                    quarterly.append({
                        "period": f"Q{((period.month-1)//3)+1} {period.year}",
                        "level": round(level, 2)
                    })

            # ------------------------
            # Yearly history
            # ------------------------
            cursor.execute("""
                SELECT
                    date_trunc('year', time) AS period,
                    AVG(water_level_m) AS avg_level
                FROM groundwater_levels
                WHERE well_id = %s
                GROUP BY period
                ORDER BY period;
            """, [well_id])

            yearly = []

            for period, level in cursor.fetchall():
                if period and level is not None:
                    yearly.append({
                        "period": str(period.year),
                        "level": round(level, 2)
                    })

            # ------------------------
            # LULC (optional)
            # ------------------------
            lulc = {
                "class": "Unknown",
                "areaHectares": None
            }

            try:
                cursor.execute("""
                    SELECT
                        lulc_class,
                        ST_Area(geom::geography)/10000
                    FROM lulc_polygons
                    WHERE ST_Contains(
                        geom,
                        ST_SetSRID(
                            ST_MakePoint(%s,%s),
                            4326
                        )
                    )
                    LIMIT 1;
                """, [well["longitude"], well["latitude"]])

                row = cursor.fetchone()

                if row:
                    lulc = {
                        "class": row[0],
                        "areaHectares": round(row[1], 1)
                    }

            except Exception:
                pass

            return Response({
                "well": well,
                "waterLevelHistory": {
                    "monthly": monthly,
                    "quarterly": quarterly,
                    "yearly": yearly
                },
                "lulc": lulc
            })

    except Exception as e:
        logger.exception("Unhandled error in view")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )