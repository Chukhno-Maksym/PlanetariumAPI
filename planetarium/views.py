from django.db.models import Count, F
from django.http import HttpResponse
from django.template.loader import render_to_string
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view, OpenApiParameter

from rest_framework import viewsets
from xhtml2pdf import pisa

from planetarium.models import (
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme
)
from planetarium.permissions import (
    IfAdminOrReadOnly,
    IsReservationAdminOrOwner,
    IsAdminOrOwner
)

from planetarium.serializers import (
    ShowSessionSerializer,
    TicketSerializer,
    ReservationSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    ShowThemeSerializer,
    ShowSessionListSerializer,
    ShowSessionDetailSerializer,
    AstronomyShowDetailSerializer,
    PlanetariumDomeDetailSerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="Get all show sessions",
        description="Returns a list of all show sessions."
    ),
    retrieve=extend_schema(
        summary="Get a specific show session",
        description="Returns details of a specific show session."
    ),
)
class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_queryset(self):
        queryset = ShowSession.objects.all()

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)

        planetarium_dome = self.request.query_params.get("planetarium_dome")
        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__id=planetarium_dome)

        min_tickets = self.request.query_params.get("min_tickets")
        max_tickets = self.request.query_params.get("max_tickets")

        if min_tickets:
            queryset = queryset.annotate(
                tickets_available=(
                    (F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")) - Count("tickets")
                )
            ).filter(tickets_available__gte=int(min_tickets))

        if max_tickets:
            queryset = queryset.annotate(
                tickets_available=(
                    (F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")) - Count("tickets")
                )
            ).filter(tickets_available__lte=int(max_tickets))

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("planetarium_dome", "astronomy_show")

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                description="Filter by session date",
                required=False,
                type=str),
            OpenApiParameter(
                name="planetarium_dome",
                description="Filter by planetarium dome",
                required=False,
                type=int),
            OpenApiParameter(
                name="min_tickets",
                description="Minimum available tickets",
                required=False,
                type=int),
            OpenApiParameter(
                name="max_tickets",
                description="Maximum available tickets",
                required=False,
                type=int
            ),
        ],
        responses={200: ShowSessionListSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        elif self.action == 'retrieve':
            return ShowSessionDetailSerializer
        return ShowSessionSerializer


@extend_schema_view(
    list=extend_schema(summary="Get all tickets"),
    retrieve=extend_schema(summary="Get a specific ticket"),
    create=extend_schema(
        summary="Create a ticket",
        description="Creates a reservation for the user and returns a PDF ticket.",
        request=TicketSerializer,
        responses={
            200: OpenApiResponse(description="PDF ticket file"),
            400: OpenApiResponse(description="Invalid request data"),
        }
    )
)
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

@extend_schema_view(
    list=extend_schema(summary="Get all reservations"),
    retrieve=extend_schema(summary="Get a specific reservation"),
    create=extend_schema(summary="Create a reservation"),
    update=extend_schema(summary="Update a reservation"),
    partial_update=extend_schema(summary="Partially update a reservation"),
    destroy=extend_schema(summary="Delete a reservation"),
)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsReservationAdminOrOwner]

@extend_schema_view(
    list=extend_schema(summary="Get all planetarium domes"),
    retrieve=extend_schema(summary="Get a specific planetarium dome"),
)
class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlanetariumDomeDetailSerializer
        return PlanetariumDomeSerializer


@extend_schema_view(
    list=extend_schema(summary="Get all astronomy shows"),
    retrieve=extend_schema(summary="Get a specific astronomy show"),
)
class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    permission_classes = [IfAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AstronomyShowDetailSerializer
        return AstronomyShowSerializer

@extend_schema_view(
    list=extend_schema(summary="Get all show themes"),
    retrieve=extend_schema(summary="Get a specific show theme"),
)
class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IfAdminOrReadOnly]
