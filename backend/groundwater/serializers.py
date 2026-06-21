from rest_framework import serializers
from .models import Pumping, WaterLevel, WaterTable, TDS, Salinity


class PumpingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pumping
        fields = '__all__'


class WaterLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLevel
        fields = '__all__'


class WaterTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterTable
        fields = '__all__'


class TDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TDS
        fields = '__all__'


class SalinitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salinity
        fields = '__all__'