from django.db import models


class Pumping(models.Model):
    hours = models.FloatField()
    crop = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.crop


class WaterLevel(models.Model):
    level = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.level)


class WaterTable(models.Model):
    depth = models.FloatField()
    date = models.DateField()


class TDS(models.Model):
    value = models.FloatField()
    date = models.DateField()


class Salinity(models.Model):
    value = models.FloatField()
    date = models.DateField()

class GISLayer(models.Model):
    name = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100, unique=True)
    original_file = models.CharField(max_length=255)
    geometry_type = models.CharField(max_length=50, blank=True)
    is_visible = models.BooleanField(default=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name