from datetime import date, timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from attendance.models import AttendanceSession, AttendanceRecord


class AttendanceApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='attendance_user',
            email='attendance_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Attendance',
            last_name='User',
        )

        cls.session = AttendanceSession.objects.create(
            title='Sunday Service',
            service_type='SUNDAY',
            session_date=date.today(),
            notes='Weekly worship attendance',
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

    def test_attendance_check_in(self):
        self.authenticate()
        response = self.client.post(f'/api/attendance/sessions/{self.session.id}/check_in/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Attendance recorded')

    def test_attendance_leaderboard(self):
        self.authenticate()
        self.client.post(f'/api/attendance/sessions/{self.session.id}/check_in/')
        response = self.client.get('/api/attendance/sessions/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
