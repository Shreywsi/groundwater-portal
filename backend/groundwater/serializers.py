from rest_framework import serializers


class WellSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    well_name = serializers.CharField()
    village = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    depth_m = serializers.FloatField()
    water_level_m = serializers.FloatField()