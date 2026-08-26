from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from church_members.models import User
from events.admin import EventAdminForm
from events.models import Event


class EventsApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user(
            username='event_user',
            email='event_user@example.com',
            password='StrongP@ssw0rd!',
            first_name='Event',
            last_name='User',
            role='MEMBER',
        )
        cls.admin = User.objects.create_user(
            username='admin_event_manager',
            email='admin_event_manager@example.com',
            password='StrongP@ssw0rd!',
            first_name='Admin',
            last_name='Manager',
            role='ADMIN_USER',
        )

        cls.event = Event.objects.create(
            title='Sunday Service',
            description='Weekly worship event.',
            event_type='SERVICE',
            event_date=timezone.now() + timedelta(days=2),
            location='Campus Chapel',
            registration_required=True,
            max_attendees=100,
            created_by=cls.admin,
            is_active=True,
        )

    def authenticate(self, user):
        response = self.client.post(
            '/api/auth/login/',
            {'username': user.username, 'password': 'StrongP@ssw0rd!'},
            format='json'
        )
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_event_list_requires_auth(self):
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_member_cannot_create_event(self):
        self.authenticate(self.member)
        payload = {
            'title': 'Unauthorised Event',
            'description': 'Should fail',
            'event_type': 'SERVICE',
            'event_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'),
            'location': 'Main Chapel',
            'registration_required': False,
            'max_attendees': 150,
            'recurrence': 'NONE',
            'recurrence_day': '',
            'recurrence_end_date': '',
        }
        response = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_event(self):
        self.authenticate(self.admin)
        payload = {
            'title': 'Weekly Sunday Service',
            'description': 'Every Sunday morning worship.',
            'event_type': 'SERVICE',
            'event_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'),
            'location': 'Main Chapel',
            'registration_required': False,
            'max_attendees': 150,
            'recurrence': 'WEEKLY',
            'recurrence_day': 'SUNDAY',
            'recurrence_end_date': (timezone.now() + timedelta(weeks=8)).date().isoformat(),
        }

        response = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recurrence'], 'WEEKLY')
        self.assertEqual(response.data['recurrence_day'], 'SUNDAY')

    def test_event_list_returns_data(self):
        self.authenticate(self.member)
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.event.title)

    def test_monthly_and_weekly_calendar_endpoints_return_events(self):
        self.authenticate(self.member)
        month_response = self.client.get(
            f'/api/events/calendar/?year={self.event.event_date.year}&month={self.event.event_date.month}'
        )
        weekly_response = self.client.get(
            f'/api/events/weekly/?date={self.event.event_date.date().isoformat()}'
        )
        self.assertEqual(month_response.status_code, status.HTTP_200_OK)
        self.assertEqual(weekly_response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item['id'] == self.event.id for item in month_response.data))
        self.assertTrue(any(item['id'] == self.event.id for item in weekly_response.data))

    def test_event_register_and_cancel(self):
        self.authenticate(self.member)
        register_response = self.client.post(f'/api/events/{self.event.id}/register/')
        self.assertEqual(register_response.status_code, status.HTTP_200_OK)
        self.assertEqual(register_response.data['message'], 'Successfully registered')

        cancel_response = self.client.post(f'/api/events/{self.event.id}/cancel_registration/')
        self.assertEqual(cancel_response.status_code, status.HTTP_200_OK)
        self.assertTrue(cancel_response.data['removed'])

    def test_registration_is_owned_by_authenticated_member(self):
        self.authenticate(self.member)
        response = self.client.post(
            '/api/events/registrations/',
            {'event': self.event.id, 'member': self.admin.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['member'], self.member.id)

    def test_member_cannot_modify_another_registration(self):
        registration = self.event.registrations.create(member=self.admin)
        self.authenticate(self.member)
        response = self.client.patch(
            f'/api/events/registrations/{registration.id}/',
            {'status': 'CANCELLED'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_weekly_recurring_event_requires_recurrence_day(self):
        self.authenticate(self.admin)

        payload = {
            'title': 'Weekly Sunday Service',
            'description': 'Every Sunday morning worship.',
            'event_type': 'SERVICE',
            'event_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'),
            'location': 'Main Chapel',
            'registration_required': False,
            'max_attendees': 150,
            'recurrence': 'WEEKLY',
        }

        response = self.client.post('/api/events/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('recurrence_day', response.data)


class EventsAdminFormTests(TestCase):

    def test_event_admin_form_accepts_time_with_hrs_suffix(self):
        creator = User.objects.create_user(
            username='admin_creator',
            email='admin_creator@example.com',
            password='StrongP@ssw0rd!',
            first_name='Admin',
            last_name='Creator',
        )

        form = EventAdminForm(data={
            'title': 'Test Event',
            'description': 'Testing event admin form.',
            'event_type': 'SERVICE',
            'event_date_0': (timezone.now() + timedelta(days=5)).date().isoformat(),
            'event_date_1': '08:00hrs',
            'location': 'Main Chapel',
            'registration_required': 'False',
            'max_attendees': '50',
            'recurrence': 'NONE',
            'recurrence_day': '',
            'recurrence_end_date': '',
            'created_by': creator.pk,
        })

        self.assertTrue(form.is_valid())
        self.assertIsNotNone(form.cleaned_data['event_date'])
        self.assertEqual(form.cleaned_data['event_date'].hour, 8)
        self.assertEqual(form.cleaned_data['event_date'].minute, 0)


class EventApiTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username='api_creator',
            email='api_creator@example.com',
            password='StrongP@ssw0rd!',
            first_name='Api',
            last_name='Creator',
            role='ADMIN_USER',
        )
        self.client.force_authenticate(user=self.admin)

    def test_api_event_creation_sets_created_by(self):
        payload = {
            'title': 'API Created Event',
            'description': 'Event created through API.',
            'event_type': 'SERVICE',
            'event_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S'),
            'location': 'Main Chapel',
            'registration_required': False,
            'max_attendees': 150,
            'recurrence': 'NONE',
            'recurrence_day': '',
            'recurrence_end_date': '',
        }

        response = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        event_id = response.data['id']
        event = Event.objects.get(pk=event_id)
        self.assertEqual(event.created_by, self.admin)
