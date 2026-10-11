from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from committees.models import Committee, CommitteeMembership
from announcements.models import Announcement


class AnnouncementsApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='announcement_user',
            email='announcement_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Announcement',
            last_name='User',
        )

        cls.announcement = Announcement.objects.create(
            title='Service Reminder',
            message='Please join the Sunday service at 9 AM.',
            target_type='ALL',
            is_active=True,
            created_by=cls.user,
        )
        cls.outside_member = User.objects.create_user(
            username='outside_member',
            email='outside_member@example.com',
            password='StrongP@ssw0rd!',
            role='MEMBER',
        )
        cls.committee_member = User.objects.create_user(
            username='committee_member',
            email='committee_member@example.com',
            password='StrongP@ssw0rd!',
            role='MEMBER',
        )
        cls.committee_leader = User.objects.create_user(
            username='committee_leader',
            email='committee_leader@example.com',
            password='StrongP@ssw0rd!',
            role='HIGH_PRIVILEGE_USER',
        )
        cls.admin = User.objects.create_user(
            username='announcement_admin',
            email='announcement_admin@example.com',
            password='StrongP@ssw0rd!',
            role='ADMIN_USER',
        )
        cls.super_user = User.objects.create_user(
            username='announcement_super',
            email='announcement_super@example.com',
            password='StrongP@ssw0rd!',
            role='SUPER_USER',
        )
        cls.committee = Committee.objects.create(name='Youth Committee')
        CommitteeMembership.objects.create(
            user=cls.committee_member,
            committee=cls.committee,
        )
        CommitteeMembership.objects.create(
            user=cls.committee_leader,
            committee=cls.committee,
            notes='Committee leader',
        )
        cls.committee_announcement = Announcement.objects.create(
            title='Committee Meeting',
            message='Committee members only.',
            target_type='COMMITTEE',
            committee=cls.committee,
            created_by=cls.admin,
        )

    def authenticate(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_announcements_list_requires_auth(self):
        response = self.client.get('/api/announcements/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_announcements_latest_returns_data(self):
        self.authenticate()
        response = self.client.get('/api/announcements/latest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.announcement.title)

    def test_committee_announcement_is_visible_only_to_members_and_privileged_roles(self):
        for user in [self.outside_member]:
            self.client.force_authenticate(user=user)
            list_response = self.client.get('/api/announcements/')
            detail_response = self.client.get(
                f'/api/announcements/{self.committee_announcement.id}/'
            )
            self.assertNotIn(
                self.committee_announcement.id,
                [item['id'] for item in list_response.data],
            )
            self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)

        for user in [
            self.committee_member,
            self.committee_leader,
            self.admin,
            self.super_user,
        ]:
            self.client.force_authenticate(user=user)
            list_response = self.client.get('/api/announcements/')
            detail_response = self.client.get(
                f'/api/announcements/{self.committee_announcement.id}/'
            )
            self.assertIn(
                self.committee_announcement.id,
                [item['id'] for item in list_response.data],
            )
            self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_only_high_privilege_or_above_can_deactivate(self):
        self.client.force_authenticate(user=self.outside_member)
        response = self.client.post(
            f'/api/announcements/{self.announcement.id}/deactivate/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.committee_leader)
        response = self.client.post(
            f'/api/announcements/{self.announcement.id}/deactivate/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
