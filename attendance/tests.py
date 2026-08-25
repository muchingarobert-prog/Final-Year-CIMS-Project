from datetime import date, timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from attendance.models import AttendanceSession, AttendanceRecord


class AttendanceApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='attendance_user',
            email='attendance_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Attendance',
            last_name='User',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='attendance_admin',
            email='attendance_admin@example.com',
            password='StrongP@ssw0rd!',
            first_name='Attendance',
            last_name='Admin',
            role='ADMIN_USER',
        )

        cls.session = AttendanceSession.objects.create(
            title='Sunday Service',
            service_type='SUNDAY',
            session_date=date.today(),
            notes='Weekly worship attendance',
            is_active=True,
            created_by=cls.admin,
        )

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_attendance_check_in(self):
        self.authenticate(self.member)
        response = self.client.post(f'/api/attendance/sessions/{self.session.id}/check_in/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Attendance recorded')

    def test_member_cannot_create_another_members_attendance(self):
        other = User.objects.create_user(
            username='other_member',
            email='other_member@example.com',
            password='StrongP@ssw0rd!',
            first_name='Other',
            last_name='Member',
            role='MEMBER',
        )
        self.authenticate(self.member)
        response = self.client.post(
            '/api/attendance/records/',
            {'member': other.id, 'session': self.session.id, 'status': 'PRESENT'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_attendance_record(self):
        self.authenticate(self.admin)
        response = self.client.post(
            '/api/attendance/records/',
            {'member': self.member.id, 'session': self.session.id, 'status': 'PRESENT'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_attendance_leaderboard(self):
        self.authenticate(self.member)
        self.client.post(f'/api/attendance/sessions/{self.session.id}/check_in/')
        response = self.client.get('/api/attendance/sessions/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
