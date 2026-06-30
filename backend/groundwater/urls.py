from django.urls import path
from .views import dashboard, open_qgis, wells, waterlevel, pumping, well_detail

urlpatterns = [
    path("dashboard/", dashboard),
    path("wells/", wells),
    path("wells/<int:well_id>/", well_detail),
    path("waterlevel/", waterlevel),
    path("pumping/", pumping),
    path("open-qgis/", open_qgis),
]