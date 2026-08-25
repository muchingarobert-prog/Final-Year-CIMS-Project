from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User


class ChurchMembersApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='StrongP@ssw0rd!',
            first_name='Member',
            last_name='One',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='admin1',
            email='admin1@example.com',
            password='StrongP@ssw0rd!',
            first_name='Admin',
            last_name='One',
            role='ADMIN_USER',
        )

    def test_user_list_requires_auth(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_member_cannot_list_users(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.member.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.admin.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_private_profile_fields_are_hidden_in_user_search(self):
        self.member.is_profile_public = False
        self.member.phone_number = '555-0100'
        self.member.programme_of_study = 'Private Programme'
        self.member.save()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/auth/search-users/?search=Member')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_user_can_access_own_profile_search_result(self):
        self.member.is_profile_public = False
        self.member.phone_number = '555-0100'
        self.member.save()
        self.client.force_authenticate(user=self.member)
        response = self.client.get('/api/auth/search-users/?search=Member')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['phone_number'], '555-0100')

    def test_member_cannot_modify_another_user_profile(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.member.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

        response = self.client.patch(
            f'/api/users/{self.admin.id}/',
            {'first_name': 'Hacker'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_cannot_change_own_role_or_admin_flags(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.member.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")

        response = self.client.patch(
            f'/api/users/{self.member.id}/',
            {'role': 'ADMIN_USER', 'is_staff': True, 'is_superuser': True, 'is_active': False},
            format='json'
        )
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, 'MEMBER')
        self.assertFalse(self.member.is_staff)
        self.assertFalse(self.member.is_superuser)
        self.assertTrue(self.member.is_active)
