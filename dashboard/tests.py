from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from notifications.models import Notification
from attendance.models import AttendanceSession, AttendanceRecord
from events.models import Event


class DashboardApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='dashboard_user',
            email='dashboard_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Dashboard',
            last_name='User',
            role='HIGH_PRIVILEGE_USER',
        )

        cls.event = Event.objects.create(
            title='Sunday Service',
            description='Weekly worship service.',
            event_type='SERVICE',
            event_date=timezone.now() + timedelta(days=2),
            location='Campus Chapel',
            registration_required=False,
            max_attendees=100,
            created_by=cls.user,
            is_active=True,
        )

        cls.session = AttendanceSession.objects.create(
            title='Sunday Service Session',
            service_type='SUNDAY',
            session_date=timezone.now().date(),
            notes='Attendance session',
            is_active=True,
            created_by=cls.user,
        )

        cls.notification = Notification.objects.create(
            recipient=cls.user,
            title='Event Reminder',
            message='Don’t forget tomorrow’s service.',
            notification_type='EVENT',
            is_read=False,
            created_at=timezone.now(),
        )

        AttendanceRecord.objects.create(
            member=cls.user,
            session=cls.session,
            status='PRESENT',
        )

    def authenticate(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_dashboard_analytics_requires_auth(self):
        response = self.client.get('/api/dashboard/analytics/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_analytics_returns_data(self):
        self.authenticate()
        response = self.client.get('/api/dashboard/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('top_attendees', response.data)
        self.assertIn('top_events', response.data)

    def test_member_cannot_access_dashboard_analytics(self):
        member = User.objects.create_user(
            username='dashboard_member',
            email='dashboard_member@example.com',
            password='StrongP@ssw0rd!',
            role='MEMBER',
        )
        self.client.force_authenticate(user=member)
        response = self.client.get('/api/dashboard/analytics/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
