from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from notifications.models import Notification


class NotificationsApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='notification_user',
            email='notification_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Notification',
            last_name='User',
        )

        cls.notification = Notification.objects.create(
            recipient=cls.user,
            title='Event Updated',
            message='The Sunday service time has changed.',
            notification_type='EVENT',
            is_read=False,
            created_at=timezone.now(),
        )

    def authenticate(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_notifications_list_requires_auth(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_notifications_unread_returns_data(self):
        self.authenticate()
        response = self.client.get('/api/notifications/unread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.notification.title)

    def test_mark_notification_read(self):
        self.authenticate()
        response = self.client.post(f'/api/notifications/{self.notification.id}/mark_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
