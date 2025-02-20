from rest_framework import viewsets

from planetarium.models import (
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme
)

from planetarium.serializers import (
    ShowSessionSerializer,
    TicketSerializer,
    ReservationSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    ShowThemeSerializer
)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer