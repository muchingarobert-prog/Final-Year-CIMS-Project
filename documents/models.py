from django.db import models
from django.conf import settings

from committees.models import Committee


class Document(models.Model):

    DOCUMENT_TYPES = [
        ('MINUTES', 'Meeting Minutes'),
        ('CONSTITUTION', 'Constitution'),
        ('REPORT', 'Report'),
        ('GUIDELINE', 'Guideline'),
        ('FINANCIAL', 'Financial Document'),
        ('CIRCULAR', 'Circular'),
        ('POLICY', 'Policy'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(
        upload_to='documents/'
    )

    committee = models.ForeignKey(
        Committee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    version = models.PositiveIntegerField(
        default=1
    )

    download_count = models.PositiveIntegerField(
        default=0
    )

    is_public = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title