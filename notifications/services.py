from django.core.mail import send_mail

from church_members.models import User

from .models import Notification


def create_notification(recipient, title, message, notification_type='SYSTEM'):
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
    )


def bulk_create_notifications(users, title, message, notification_type='SYSTEM'):
    notifications = [
        Notification(
            recipient=user,
            title=title,
            message=message,
            notification_type=notification_type,
        )
        for user in users
    ]
    return Notification.objects.bulk_create(notifications)


def notify_all_members(title, message, notification_type='SYSTEM'):
    return bulk_create_notifications(
        User.objects.filter(is_active=True),
        title,
        message,
        notification_type,
    )


def send_email_notification(subject, message, recipients, from_email=None):
    return send_mail(
        subject,
        message,
        from_email,
        recipients,
        fail_silently=True,
    )


def send_sms_notification(phone_number, message):
    """SMS integration placeholder; returns the queued payload."""
    return {
        'phone_number': phone_number,
        'message': message,
        'sent': False,
    }


def mark_notifications_read(user):
    return Notification.objects.filter(
        recipient=user,
        is_read=False,
    ).update(is_read=True)
