from rest_framework import viewsets
from .models import Pumping, WaterLevel, WaterTable, TDS, Salinity
from .serializers import (
    PumpingSerializer,
    WaterLevelSerializer,
    WaterTableSerializer,
    TDSSerializer,
    SalinitySerializer
)


class PumpingViewSet(viewsets.ModelViewSet):
    queryset = Pumping.objects.all()
    serializer_class = PumpingSerializer


class WaterLevelViewSet(viewsets.ModelViewSet):
    queryset = WaterLevel.objects.all()
    serializer_class = WaterLevelSerializer


class WaterTableViewSet(viewsets.ModelViewSet):
    queryset = WaterTable.objects.all()
    serializer_class = WaterTableSerializer


class TDSViewSet(viewsets.ModelViewSet):
    queryset = TDS.objects.all()
    serializer_class = TDSSerializer


class SalinityViewSet(viewsets.ModelViewSet):
    queryset = Salinity.objects.all()
    serializer_class = SalinitySerializer