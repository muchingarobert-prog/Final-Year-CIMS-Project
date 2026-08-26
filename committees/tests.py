from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from committees.models import Committee, CommitteeMembership


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

    def test_committee_join_request_and_member_statistics(self):
        self.authenticate()
        join_response = self.client.post(f'/api/committees/{self.committee.id}/join/')
        self.assertEqual(join_response.status_code, status.HTTP_202_ACCEPTED)
        membership = CommitteeMembership.objects.get(
            committee=self.committee,
            user=self.user,
        )
        self.assertFalse(membership.is_active)
        stats_response = self.client.get(
            f'/api/committees/{self.committee.id}/member_statistics/'
        )
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data['members'], 0)
