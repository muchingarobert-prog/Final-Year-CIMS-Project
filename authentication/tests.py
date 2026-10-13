from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.test import override_settings
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from committees.models import Committee
from events.models import Event


class CoreApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='StrongP@ssw0rd!',
            first_name='Member',
            last_name='One',
        )

        cls.committee = Committee.objects.create(
            name='Worship Committee',
            description='Coordinates worship and music.',
            purpose='Organize worship sessions',
            meeting_schedule='Sundays after service',
            is_active=True,
        )

        cls.event = Event.objects.create(
            title='Sunday Service',
            description='Weekly worship service for the congregation.',
            event_type='SERVICE',
            event_date=timezone.now() + timedelta(days=2),
            location='Campus Chapel',
            registration_required=False,
            max_attendees=200,
            created_by=cls.user,
            is_active=True,
        )

    def test_register_user(self):
        url = '/api/auth/register/'
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Str0ngPassw0rd!',
            'first_name': 'New',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '2000-01-01',
            'phone_number': '+260971234567',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_returns_tokens(self):
        url = '/api/auth/login/'
        payload = {
            'username': self.user.username,
            'password': 'StrongP@ssw0rd!',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']

    def test_refresh_endpoint_returns_access_token(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json',
        )

        response = self.client.post(
            '/api/auth/token/refresh/',
            {'refresh': login_response.data['refresh']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_jwt_lifetimes_are_practice_friendly_and_finite(self):
        self.assertEqual(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], timedelta(minutes=30))
        self.assertEqual(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], timedelta(days=7))

    def test_dashboard_requires_auth(self):
        url = '/api/auth/dashboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_returns_user_statistics(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get('/api/auth/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('statistics', response.data)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_committees_list_requires_auth(self):
        response = self.client.get('/api/committees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_committees_list_returns_data(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get('/api/committees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.committee.name)

    def test_events_list_requires_auth(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_events_list_returns_data(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        response_titles = [item.get('title') for item in response.data]
        self.assertIn(self.event.title, response_titles)

    @override_settings(
        PASSWORD_RESET_FRONTEND_URL='https://cims.example/reset-password'
    )
    @patch('authentication.views.send_mail')
    def test_password_reset_response_is_generic_and_link_is_configurable(
        self,
        send_mail,
    ):
        known_response = self.client.post(
            '/api/auth/password-reset/',
            {'email': self.user.email},
            format='json',
        )
        unknown_response = self.client.post(
            '/api/auth/password-reset/',
            {'email': 'missing@example.com'},
            format='json',
        )

        self.assertEqual(known_response.status_code, unknown_response.status_code)
        self.assertEqual(known_response.data, unknown_response.data)
        self.assertEqual(known_response.data['message'], 'If that email exists, a reset link has been sent.')
        self.assertIn('https://cims.example/reset-password/', send_mail.call_args[1]['message'])

    def test_password_reset_confirm_rejects_malformed_user_id(self):
        response = self.client.post(
            '/api/auth/password-reset-confirm/not-valid/token/',
            {'password': 'NewStr0ngPassw0rd!'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
