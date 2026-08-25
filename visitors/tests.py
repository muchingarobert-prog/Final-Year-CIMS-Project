from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User


class VisitorSecurityTests(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.member = User.objects.create_user(
			username='visitor_member',
			email='visitor_member@example.com',
			password='StrongP@ssw0rd!',
			role='MEMBER',
		)
		cls.staff = User.objects.create_user(
			username='visitor_staff',
			email='visitor_staff@example.com',
			password='StrongP@ssw0rd!',
			role='HIGH_PRIVILEGE_USER',
		)

	def test_member_cannot_access_visitors(self):
		self.client.force_authenticate(user=self.member)
		response = self.client.get('/api/visitors/')
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_high_privilege_user_can_access_visitors(self):
		self.client.force_authenticate(user=self.staff)
		response = self.client.get('/api/visitors/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
