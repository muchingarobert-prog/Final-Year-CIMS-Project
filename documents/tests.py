from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from documents.models import Document


class DocumentSecurityTests(APITestCase):

	@classmethod
	def setUpTestData(cls):
		cls.owner = User.objects.create_user(
			username='document_owner',
			email='document_owner@example.com',
			password='StrongP@ssw0rd!',
			role='MEMBER',
		)
		cls.other = User.objects.create_user(
			username='document_other',
			email='document_other@example.com',
			password='StrongP@ssw0rd!',
			role='MEMBER',
		)
		cls.private_document = Document.objects.create(
			title='Private document',
			description='Private',
			document_type='OTHER',
			file=SimpleUploadedFile('private.txt', b'private'),
			uploaded_by=cls.owner,
			is_public=False,
		)

	def test_private_document_is_hidden_from_other_member(self):
		self.client.force_authenticate(user=self.other)
		response = self.client.get(f'/api/documents/{self.private_document.id}/')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_uploader_can_access_private_document(self):
		self.client.force_authenticate(user=self.owner)
		response = self.client.get(f'/api/documents/{self.private_document.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_document_upload_rejects_unsupported_extension(self):
		self.client.force_authenticate(user=self.owner)
		response = self.client.post(
			'/api/documents/',
			{
				'title': 'Unsafe document',
				'document_type': 'OTHER',
				'file': SimpleUploadedFile('payload.exe', b'not allowed'),
			},
			format='multipart',
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
