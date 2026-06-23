from django.db import models
from django.conf import settings


class Committee(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    purpose = models.TextField(
        blank=True
    )

    meeting_schedule = models.CharField(
        max_length=255,
        blank=True
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
        return self.name


class CommitteePosition(models.Model):

    POSITION_TYPES = [

        ('CHAIRPERSON', 'Chairperson'),

        ('VICE_CHAIRPERSON',
         'Vice Chairperson'),

        ('SECRETARY',
         'Secretary'),

        ('VICE_SECRETARY',
         'Vice Secretary'),

        ('TREASURER',
         'Treasurer'),

        ('VICE_TREASURER',
         'Vice Treasurer'),

        ('MEMBER',
         'Member'),
    ]

    title = models.CharField(
        max_length=100,
        unique=True
    )

    position_type = models.CharField(
        max_length=30,
        choices=POSITION_TYPES,
        default='MEMBER'
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.title


class CommitteeMembership(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='committee_memberships'
    )

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    position = models.ForeignKey(
        CommitteePosition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    joined_date = models.DateField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    notes = models.TextField(
        blank=True
    )

    class Meta:

        unique_together = (
            'user',
            'committee',
        )

    def __str__(self):

        return (
            f"{self.user} - "
            f"{self.committee}"
        )