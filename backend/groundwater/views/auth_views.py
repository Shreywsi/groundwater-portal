import os
import subprocess

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from ..models import UserProfile

import logging

logger = logging.getLogger(__name__)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def open_qgis(request):

    qgis_project = os.path.join(
        settings.BASE_DIR,
        "qgis",
        "WaterManagement.qgz"
    )

    try:
        subprocess.Popen([
            "open",
            "-a",
            "QGIS",
            qgis_project
        ])

        return Response({
            "success": True,
            "message": "QGIS launched successfully."
        })

    except Exception as e:
        return Response({
            "success": False,
            "message": str(e)
        }, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = str(request.data.get("username", "")).strip()
    password = str(request.data.get("password", ""))
    #role = str(request.data.get("role", "")).strip()

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {
                "success": False,
                "error": "Invalid username or password.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)

    try:
        profile = UserProfile.objects.get(user=user)
        user_role = profile.role
    except UserProfile.DoesNotExist:
        user_role = "crp"

    return Response({
        "success": True,
        "token": token.key,
        "username": user.username,
        "role": user_role,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

    full_name = request.data.get("full_name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role")

    if not all([full_name, username, email, password, role]):
        return Response({
            "success": False,
            "error": "All fields are required."
        }, status=400)

    if User.objects.filter(username=username).exists():
        return Response({
            "success": False,
            "error": "Username already exists."
        }, status=400)

    if User.objects.filter(email=email).exists():
        return Response({
            "success": False,
            "error": "Email already exists."
        }, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=full_name
    )

    UserProfile.objects.create(
        user=user,
        full_name=full_name,
        role=role
    )

    return Response({
        "success": True,
        "message": "Registration successful."
    }, status=201)