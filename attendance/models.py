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
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    def __str__(self):
        return f"{self.member} - {self.status}"