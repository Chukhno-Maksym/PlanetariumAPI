import os

from django.conf import settings
from django.db.models import Count, F
from django.http import HttpResponse
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation = Reservation.objects.create(user=request.user)
        ticket = serializer.save(reservation=reservation)

        html_content = render_to_string('ticket.html', {'ticket': ticket})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        return response

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
