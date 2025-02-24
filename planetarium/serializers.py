from django.db import transaction
from rest_framework import serializers

import user
from planetarium.models import (
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme
)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name")


class PlanetariumDomeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "planetarium_dome_capacity")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description")


class AstronomyShowDetailSerializer(serializers.ModelSerializer):
    theme = ShowThemeSerializer(many=True, read_only=False)
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "theme")


class ShowSessionSerializer(serializers.ModelSerializer):
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "show_time", "astronomy_show", "planetarium_dome", "tickets_available")


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = serializers.SlugRelatedField(many=False, read_only=True, slug_field="title")
    planetarium_dome = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = ShowSession
        fields = ("id", "show_time", "astronomy_show", "planetarium_dome", "tickets_available")


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowDetailSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)
    class Meta:
        model = ShowSession
        fields = ("id", "show_time", "astronomy_show", "planetarium_dome", "tickets_available")


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="username")

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")

    def create(self, validated_data):
        with transaction.atomic():
            reservation = validated_data.pop("reservation")
            ticket = Ticket.objects.create(reservation=reservation, **validated_data)
            return ticket

