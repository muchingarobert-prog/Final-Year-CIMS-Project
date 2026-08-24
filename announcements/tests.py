from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from announcements.models import Announcement


class AnnouncementsApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='announcement_user',
            email='announcement_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Announcement',
            last_name='User',
        )

        cls.announcement = Announcement.objects.create(
            title='Service Reminder',
            message='Please join the Sunday service at 9 AM.',
            target_type='ALL',
            is_active=True,
            created_by=cls.user,
        )

    def authenticate(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_announcements_list_requires_auth(self):
        response = self.client.get('/api/announcements/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_announcements_latest_returns_data(self):
        self.authenticate()
        response = self.client.get('/api/announcements/latest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.announcement.title)
