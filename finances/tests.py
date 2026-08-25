from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from finances.models import FinancialCategory, Expense, Income


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

    def test_member_cannot_create_or_approve_expense(self):
        self.authenticate(self.member)
        create_response = self.client.post(
            '/api/finances/expenses/',
            {
                'title': 'Restricted expense',
                'category': self.category.id,
                'amount': '50.00',
                'description': 'Should fail',
            },
            format='json',
        )
        expense = Expense.objects.create(
            title='Pending expense',
            category=self.category,
            amount='25.00',
            requested_by=self.admin,
        )
        approve_response = self.client.post(
            f'/api/finances/expenses/{expense.id}/approve/'
        )
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approved_by_cannot_be_client_controlled(self):
        self.authenticate(self.admin)
        response = self.client.post(
            '/api/finances/expenses/',
            {
                'title': 'Expense request',
                'category': self.category.id,
                'amount': '25.00',
                'approved_by': self.member.id,
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Expense.objects.get(id=response.data['id']).approved_by)
