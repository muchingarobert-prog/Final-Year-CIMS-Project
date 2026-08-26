from datetime import date

from .services import create_birthday_reminders


def send_birthday_reminders(day=None):
    """Task-compatible birthday reminder entry point."""
    return create_birthday_reminders(day or date.today())
