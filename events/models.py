from django.db import models
from church_members.models import Member


class Event(models.Model):

    EVENT_TYPES = [
        ('SERVICE', 'Church Service'),
        ('YOUTH', 'Youth Activity'),
        ('COMMITTEE', 'Committee Meeting'),
        ('OUTREACH', 'Outreach Program'),
        ('CHOIR', 'Choir Activity'),
        ('SPECIAL', 'Special Event'),
    ]

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    location = models.CharField(
        max_length=255
    )

    organizer = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    registration_required = models.BooleanField(
        default=False
    )

    attendees = models.ManyToManyField(
        Member,
        blank=True,
        related_name='registered_events'
    )

    def __str__(self):
        return self.title