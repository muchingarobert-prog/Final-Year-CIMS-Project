from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from audit.models import AuditLog


class AuditAccessTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='audit_member',
            email='audit_member@example.com',
            password='StrongP@ssw0rd!',
            first_name='Audit',
            last_name='Member',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='audit_admin',
            email='audit_admin@example.com',
            password='StrongP@ssw0rd!',
            first_name='Audit',
            last_name='Admin',
            role='ADMIN_USER',
        )
        AuditLog.objects.create(user=cls.admin, action='LOGIN', module='auth', description='Test login')

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_member_cannot_access_audit_logs(self):
        self.authenticate(self.member)
        response = self.client.get('/api/audit/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_audit_logs(self):
        self.authenticate(self.admin)
        response = self.client.get('/api/audit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
