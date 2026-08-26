from datetime import date, timedelta

from .models import User
from notifications.services import bulk_create_notifications


def birthdays_on(day=None):
    day = day or date.today()
    return User.objects.filter(
        date_of_birth__month=day.month,
        date_of_birth__day=day.day,
        is_active=True,
    )


def birthdays_between(start, end):
    users = User.objects.exclude(date_of_birth=None).filter(is_active=True)
    days = set()
    current = start
    while current <= end:
        days.add((current.month, current.day))
        current += timedelta(days=1)
    return [
        user for user in users
        if (user.date_of_birth.month, user.date_of_birth.day) in days
    ]


def create_birthday_reminders(day=None):
    users = birthdays_on(day)
    return bulk_create_notifications(
        users,
        'Birthday reminder',
        'Wishing you a blessed birthday.',
        'BIRTHDAY',
    )
