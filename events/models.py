from django.db import models
from church_members.models import Member


class Event(models.Model):

    EVENT_TYPES = [
        ('SERVICE', 'Service'),
        ('MEETING', 'Meeting'),
        ('YOUTH', 'Youth Program'),
        ('SPECIAL', 'Special Event'),
    ]

    title = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    registration_required = models.BooleanField(
        default=False
    )

    attendees = models.ManyToManyField(
        Member,
        through='EventRegistration',
        blank=True
    )

    def __str__(self):
        return self.title


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
        Member,
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