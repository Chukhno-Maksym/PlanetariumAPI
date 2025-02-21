from django.urls import path, include
from rest_framework import routers

from planetarium.views import (
    ShowSessionViewSet,
    TicketViewSet,
    ReservationViewSet,
    PlanetariumDomeViewSet,
    AstronomyShowViewSet,
    ShowThemeViewSet,
)

router = routers.DefaultRouter()

router.register('show-session', ShowSessionViewSet)
router.register('tickets', TicketViewSet)
router.register('reservation', ReservationViewSet)
router.register('planetarium-dome', PlanetariumDomeViewSet)
router.register('astronomy-show', AstronomyShowViewSet)
router.register('show-theme', ShowThemeViewSet)

urlpatterns = [path('', include(router.urls))]

app_name = 'planetarium'