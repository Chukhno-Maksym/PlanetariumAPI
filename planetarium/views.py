from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from planetarium.models import (
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme
)
from planetarium.permissions import IfAdminOrReadOnly, IsReservationAdminOrOwner, IsAdminOrOwner

from planetarium.serializers import (
    ShowSessionSerializer,
    TicketSerializer,
    ReservationSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    ShowThemeSerializer, ShowSessionListSerializer, ShowSessionDetailSerializer, AstronomyShowDetailSerializer,
    PlanetariumDomeDetailSerializer
)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = (
                queryset
                .annotate(
                    tickets_available=(
                        (F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")) - Count("tickets")
                    )
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        elif self.action == 'retrieve':
            return ShowSessionDetailSerializer
        return ShowSessionSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrOwner]

    def perform_create(self, serializer):
        reservation = Reservation.objects.create(user=self.request.user)
        serializer.save(reservation=reservation)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsReservationAdminOrOwner]


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanetariumDomeDetailSerializer
        return PlanetariumDomeSerializer



class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AstronomyShowDetailSerializer
        return AstronomyShowSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IfAdminOrReadOnly]