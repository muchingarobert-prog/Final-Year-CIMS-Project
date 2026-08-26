from .services import follow_up_reminder_payload


def send_follow_up_reminders():
    """Task-compatible visitor follow-up reminder entry point."""
    return follow_up_reminder_payload()
