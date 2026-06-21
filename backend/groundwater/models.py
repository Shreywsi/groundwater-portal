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
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.depth)


class TDS(models.Model):
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.value)


class Salinity(models.Model):
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.value)