from rest_framework.routers import DefaultRouter
from .views import (
    PumpingViewSet,
    WaterLevelViewSet,
    WaterTableViewSet,
    TDSViewSet,
    SalinityViewSet
)

router = DefaultRouter()

router.register(r'pumping', PumpingViewSet)
router.register(r'waterlevel', WaterLevelViewSet)
router.register(r'watertable', WaterTableViewSet)
router.register(r'tds', TDSViewSet)
router.register(r'salinity', SalinityViewSet)

urlpatterns = router.urls