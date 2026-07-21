from django.db import models
from django.contrib.auth.models import User


# ----------------------------
# LOCATION
# ----------------------------

class Location(models.Model):

    LOCATION_TYPES = [
        ("Village", "Village"),
        ("Town", "Town"),
        ("City", "City"),
        ("Taluka", "Taluka"),
        ("District", "District"),
        ("Watershed", "Watershed"),
        ("River Basin", "River Basin"),
    ]

    name = models.CharField(max_length=200)

    location_type = models.CharField(
        max_length=30,
        choices=LOCATION_TYPES,
        default="Village",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    district = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    state = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# PUMPING
# ----------------------------

class Pumping(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="pumping_records",
    )

    hours = models.FloatField()

    crop = models.CharField(max_length=100)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.hours} hrs"


# ----------------------------
# WATER LEVEL
# ----------------------------

class WaterLevel(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="water_levels",
    )

    level = models.FloatField()

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.level}"


# ----------------------------
# WATER TABLE
# ----------------------------

class WaterTable(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="water_tables",
    )

    depth = models.FloatField()

    date = models.DateField()


# ----------------------------
# TDS
# ----------------------------

class TDS(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="tds_records",
    )

    value = models.FloatField()

    date = models.DateField()


# ----------------------------
# SALINITY
# ----------------------------

class Salinity(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="salinity_records",
    )

    value = models.FloatField()

    date = models.DateField()


# ----------------------------
# GIS LAYER
# ----------------------------

class GISLayer(models.Model):

    name = models.CharField(max_length=100)

    table_name = models.CharField(max_length=100, unique=True)

    original_file = models.CharField(max_length=255)

    geometry_type = models.CharField(max_length=50, blank=True)

    is_visible = models.BooleanField(default=True)

    imported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# USER PROFILE
# ----------------------------

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("crp", "Community Resource Person"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(max_length=150)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="crp",
    )

    def __str__(self):
        return f"{self.full_name} ({self.role})"


# ----------------------------
# WATER BALANCE
# ----------------------------

class WaterBalance(models.Model):

    location = models.ForeignKey(
        "Location",
        on_delete=models.CASCADE,
        related_name="water_balances",
        null=True,
        blank=True,
    )

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
        return f"{self.location} - {self.created_at.date()}"


# ----------------------------
# DATASET
# ----------------------------

class Dataset(models.Model):

    name = models.CharField(max_length=255)

    file_name = models.CharField(max_length=255)

    file_path = models.TextField()

    rows = models.IntegerField(default=0)

    columns = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name