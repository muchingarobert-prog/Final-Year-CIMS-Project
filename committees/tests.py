from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from committees.models import Committee


class CommitteesApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='committee_user',
            email='committee_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Committee',
            last_name='User',
        )

        cls.committee = Committee.objects.create(
            name='Worship Committee',
            description='Coordinates worship and music.',
            purpose='Organize worship sessions',
            meeting_schedule='Sundays after service',
            is_active=True,
        )

    def authenticate(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_committee_list_requires_auth(self):
        response = self.client.get('/api/committees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_committee_list_returns_data(self):
        self.authenticate()
        response = self.client.get('/api/committees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.committee.name)

    def test_committee_analytics_returns_counts(self):
        self.authenticate()
        response = self.client.get('/api/committees/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.committee.id)
        self.assertEqual(response.data[0]['members'], 0)
