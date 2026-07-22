from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Location

import logging

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_location(request):

    name = request.data.get("name", "").strip()

    if not name:
        return Response(
            {
                "success": False,
                "message": "Location name is required."
            },
            status=400
        )

    # Prevent duplicate locations
    if Location.objects.filter(name__iexact=name).exists():
        return Response(
            {
                "success": False,
                "message": "Location already exists."
            },
            status=400
        )

    location = Location.objects.create(
        name=name
    )

    return Response(
        {
            "success": True,
            "id": location.id,
            "name": location.name
        }
    )


@api_view(["GET"])
def location_list(request):
    locations = Location.objects.all().order_by("name")

    data = [
        {
            "id": location.id,
            "name": location.name,
            "location_type": location.location_type,
            "district": location.district,
            "state": location.state,
            "parent": location.parent.id if location.parent else None,
        }
        for location in locations
    ]

    return Response(data)


@api_view(["DELETE"])
def delete_location(request, id):

    try:
        location = Location.objects.get(id=id)

    except Location.DoesNotExist:

        return Response(
            {
                "success": False,
                "message": "Location not found."
            },
            status=404
        )

    location.delete()

    return Response(
        {
            "success": True,
            "message": "Location deleted."
        }
    )