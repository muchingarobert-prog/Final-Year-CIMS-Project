from django.db import models
from django.conf import settings
from committees.models import Committee


class Announcement(models.Model):

    TARGET_CHOICES = [
        ('ALL', 'All Members'),
        ('COMMITTEE', 'Committee Members'),
    ]

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default='ALL'
    )

    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
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

            from notifications.models import Notification
            from church_members.models import User

            if self.target_type == 'ALL':

                users = User.objects.all()

            else:

                users = User.objects.filter(
                    committees=self.committee
                )

            notifications = []

            for user in users:

                notifications.append(
                    Notification(
                        recipient=user,
                        title=self.title,
                        message=self.message,
                        notification_type='ANNOUNCEMENT'
                    )
                )

            Notification.objects.bulk_create(
                notifications
            )