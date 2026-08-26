from datetime import date

from .models import Visitor


def visitors_due_for_follow_up(day=None):
    day = day or date.today()
    return Visitor.objects.filter(
        visit_date__lte=day,
        follow_up_status__in=['PENDING', 'CONTACTED'],
    )


def follow_up_reminder_payload(day=None):
    return [
        {
            'visitor_id': visitor.id,
            'name': str(visitor),
            'follow_up_status': visitor.follow_up_status,
        }
        for visitor in visitors_due_for_follow_up(day)
    ]
