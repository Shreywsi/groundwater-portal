from django.db import models
from django.contrib.auth.models import User

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
class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("crp", "Community Resource Person"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=150)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="crp"
    )

    def __str__(self):
        return f"{self.full_name} ({self.role})"
class WaterBalance(models.Model):
    date = models.DateField(auto_now_add=True)

    Rr = models.FloatField(default=0)
    Re = models.FloatField(default=0)
    Ri = models.FloatField(default=0)
    I = models.FloatField(default=0)
    Si = models.FloatField(default=0)

    Se = models.FloatField(default=0)
    O = models.FloatField(default=0)
    Et = models.FloatField(default=0)
    Dp = models.FloatField(default=0)

    delta_s = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Water Balance ({self.date})"