from django.contrib import admin
from .models import (
    Pumping,
    WaterTable,
    WaterLevel,
    TDS,
    Salinity
)

admin.site.register(Pumping)
admin.site.register(WaterTable)
admin.site.register(WaterLevel)
admin.site.register(TDS)
admin.site.register(Salinity)