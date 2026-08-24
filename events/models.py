from django.conf import settings
from django.db import models


class Event(models.Model):

    EVENT_TYPES = [
        ('SERVICE', 'Service'),
        ('MEETING', 'Meeting'),
        ('YOUTH', 'Youth Program'),
        ('SPECIAL', 'Special Event'),
    ]

    RECURRENCE_CHOICES = [
        ('NONE', 'None'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    DAY_OF_WEEK_CHOICES = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    event_date = models.DateTimeField(
        help_text='Enter the date and time for the event. Example: 2026-07-06 09:00 or 2026-07-06T09:00:00Z'
    )

    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default='NONE',
        help_text='Set a repeat pattern for events that occur on the same schedule each week or day.',
    )

    recurrence_day = models.CharField(
        max_length=10,
        choices=DAY_OF_WEEK_CHOICES,
        blank=True,
        default='',
        help_text='Use this for weekly recurring events to specify the repeating weekday.',
    )

    recurrence_end_date = models.DateField(
        null=True,
        blank=True,
        help_text='Optional end date for recurring events. Leave blank for an open recurrence.',
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    registration_required = models.BooleanField(
        default=False
    )

    max_attendees = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventRegistration',
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:

            from church_members.models import User
            from notifications.models import Notification

            users = User.objects.all()

            notifications = []

            for user in users:

                notifications.append(
                    Notification(
                        recipient=user,
                        title=f"New Event: {self.title}",
                        message=self.description,
                        notification_type='EVENT'
                    )
                )

            Notification.objects.bulk_create(
                notifications
            )


class EventRegistration(models.Model):

    STATUS_CHOICES = [
        ('REGISTERED', 'Registered'),
        ('ATTENDED', 'Attended'),
        ('CANCELLED', 'Cancelled'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REGISTERED'
    )

    class Meta:
        unique_together = (
            'event',
            'member',
        )

    def __str__(self):
        return f"{self.member} - {self.event}"
        