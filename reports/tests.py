from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User


class ReportAccessTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='report_member',
            email='report_member@example.com',
            password='StrongP@ssw0rd!',
            first_name='Report',
            last_name='Member',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='report_admin',
            email='report_admin@example.com',
            password='StrongP@ssw0rd!',
            first_name='Report',
            last_name='Admin',
            role='ADMIN_USER',
        )

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_member_cannot_access_congregation_reports(self):
        self.authenticate(self.member)
        response = self.client.get('/api/reports/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_congregation_reports(self):
        self.authenticate(self.admin)
        response = self.client.get('/api/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
