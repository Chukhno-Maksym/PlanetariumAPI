from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from planetarium.models import ShowSession, Ticket, Reservation, PlanetariumDome, AstronomyShow
from django.contrib.auth import get_user_model

User = get_user_model()

class ShowSessionViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Dome 1",
            rows=10,
            seats_in_row=10
        )

        self.astronomy_show = AstronomyShow.objects.create(
            title="Show 1",
            description="Description"

        )
        self.show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time="2025-02-25 12:00:00"
        )

        self.url = reverse('planetarium:show-session-list')

    def test_show_sessions_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_filter_by_date(self):
        response = self.client.get(
            self.url,
            {'show_time': '2025-02-25'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_filter_by_dome(self):
        response = self.client.get(self.url, {'planetarium_dome': self.planetarium_dome.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TicketViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Dome 1",
            rows=10,
            seats_in_row=10
        )
        self.astronomy_show = AstronomyShow.objects.create(
            title="Show 1",
            description="Description"
        )
        self.show_session = ShowSession.objects.create(
            astronomy_show=self.astronomy_show,
            planetarium_dome=self.planetarium_dome,
            show_time="2025-02-25 12:00:00"
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.url = reverse('planetarium:ticket-list')

    def test_create_ticket_success(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'row': 5,
            'seat': 6,
            'show_session': self.show_session.id,
            'reservation': self.reservation.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket_invalid_row(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'row': 15,
            'seat': 6,
            'show_session': self.show_session.id,
            'reservation': self.reservation.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_invalid_seat(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'row': 5,
            'seat': 15,
            'show_session': self.show_session.id,
            'reservation': self.reservation.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_no_available_seat(self):
        self.client.force_authenticate(user=self.user)

        Ticket.objects.create(
            row=5,
            seat=6,
            show_session=self.show_session,
            reservation=self.reservation
        )

        data = {
            'row': 5,
            'seat': 6,
            'show_session': self.show_session.id,
            'reservation': self.reservation.id
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ReservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('planetarium:reservation-list')

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user)  # Оновлено

        response = self.client.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.first().user, self.user)
