from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User


class ChurchMembersApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='StrongP@ssw0rd!',
            first_name='Member',
            last_name='One',
        )

    def test_user_list_requires_auth(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_returns_users(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)
