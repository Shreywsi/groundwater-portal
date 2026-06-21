from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("", lambda request: HttpResponse("Water Management Backend Running")),
    path("admin/", admin.site.urls),
    path("api/", include("groundwater.urls")),
]