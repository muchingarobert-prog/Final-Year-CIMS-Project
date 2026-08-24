from datetime import timedelta

from django.utils import timezone
from django.urls import reverse

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
