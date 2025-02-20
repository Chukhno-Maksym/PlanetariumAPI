from django.core.validators import MinValueValidator
from django.db import models

from planetarium_service import settings


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey('AstronomyShow', on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey('PlanetariumDome', on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        unique_together = ('planetarium_dome', 'show_time')


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey("ShowSession", on_delete=models.CASCADE)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('row', 'seat', 'show_session')


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=127)
    seat = models.IntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.IntegerField(validators=[MinValueValidator(1)])


class AstronomyShow(models.Model):
    title = models.CharField(max_length=127)
    description = models.TextField(blank=True)
    theme = models.ManyToManyField("ShowTheme", related_name="shows")


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)
