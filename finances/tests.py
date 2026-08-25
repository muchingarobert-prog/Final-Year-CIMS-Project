from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from finances.models import FinancialCategory


class FinancePermissionsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='finance_member',
            email='finance_member@example.com',
            password='StrongP@ssw0rd!',
            first_name='Finance',
            last_name='Member',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='finance_admin',
            email='finance_admin@example.com',
            password='StrongP@ssw0rd!',
            first_name='Finance',
            last_name='Admin',
            role='ADMIN_USER',
        )
        cls.category = FinancialCategory.objects.create(
            name='Tithe',
            category_type='TITHE',
            description='Tithe contribution',
        )

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_member_cannot_create_financial_record(self):
        self.authenticate(self.member)
        response = self.client.post(
            '/api/finances/income/',
            {'member': self.member.id, 'category': self.category.id, 'amount': '50.00', 'payment_method': 'CASH'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_financial_record(self):
        self.authenticate(self.admin)
        response = self.client.post(
            '/api/finances/income/',
            {'member': self.member.id, 'category': self.category.id, 'amount': '50.00', 'payment_method': 'CASH'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
