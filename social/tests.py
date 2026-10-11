from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from church_members.models import User
from social.models import Post


class SocialSecurityTests(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.member = User.objects.create_user(
			username='social_member',
			email='social_member@example.com',
			password='StrongP@ssw0rd!',
			role='MEMBER',
		)
		cls.other = User.objects.create_user(
			username='social_other',
			email='social_other@example.com',
			password='StrongP@ssw0rd!',
			role='MEMBER',
		)
		cls.high_privilege = User.objects.create_user(
			username='social_high',
			email='social_high@example.com',
			password='StrongP@ssw0rd!',
			role='HIGH_PRIVILEGE_USER',
		)
		cls.private_post = Post.objects.create(
			title='Private',
			content='Private content',
			author=cls.other,
			privacy='PRIVATE',
		)

	def authenticate(self):
		self.client.force_authenticate(user=self.member)

	def test_private_posts_are_hidden_from_other_members(self):
		self.authenticate()
		response = self.client.get('/api/social/posts/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotIn(self.private_post.id, [item['id'] for item in response.data])

	def test_post_author_cannot_be_spoofed(self):
		self.authenticate()
		response = self.client.post(
			'/api/social/posts/',
			{
				'title': 'Owned post',
				'content': 'Content',
				'author': self.other.id,
				'privacy': 'MEMBERS',
			},
			format='json',
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Post.objects.get(id=response.data['id']).author, self.member)

	def test_gallery_upload_rejects_unsupported_extension(self):
		self.client.force_authenticate(user=self.high_privilege)
		response = self.client.post(
			'/api/social/gallery/',
			{
				'title': 'Unsafe upload',
				'file': SimpleUploadedFile('payload.exe', b'not allowed'),
			},
			format='multipart',
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
