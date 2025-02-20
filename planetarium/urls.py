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

router.register('show_session', ShowSessionViewSet)
router.register('tickets', TicketViewSet)
router.register('reservation', ReservationViewSet)
router.register('planetarium_dome', PlanetariumDomeViewSet)
router.register('astronomy_show', AstronomyShowViewSet)
router.register('show_theme', ShowThemeViewSet)

urlpatterns = [path('', include(router.urls))]

app_name = 'planetarium'