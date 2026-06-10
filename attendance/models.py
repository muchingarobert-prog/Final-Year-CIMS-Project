from django.db import models
from django.conf import settings


class AttendanceSession(models.Model):

    SERVICE_TYPES = [
        ('SUNDAY', 'Sunday Service'),
        ('MIDWEEK', 'Midweek Service'),
        ('YOUTH', 'Youth Service'),
        ('CHOIR', 'Choir Practice'),
        ('COMMITTEE', 'Committee Meeting'),
        ('SPECIAL', 'Special Program'),
    ]

    title = models.CharField(
        max_length=100
    )

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPES
    )

    session_date = models.DateField()

    notes = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_sessions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.title} - {self.session_date}"


class AttendanceRecord(models.Model):

    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('EXCUSED', 'Excused'),
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    remarks = models.TextField(
        blank=True
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'member',
            'session',
        )

    def __str__(self):
        return f"{self.member} - {self.status}"