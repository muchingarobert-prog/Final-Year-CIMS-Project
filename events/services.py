from copy import copy
import calendar
from datetime import timedelta, timezone as datetime_timezone

from django.utils import timezone


def expand_recurring_events(events, start, end):
    occurrences = []
    for event in events:
        occurrence = event.event_date
        recurrence = event.recurrence
        while occurrence < start:
            occurrence = _next_occurrence(event, occurrence)
            if recurrence == 'NONE':
                break
        while occurrence < end:
            if event.recurrence_end_date and occurrence.date() > event.recurrence_end_date:
                break
            if occurrence >= start:
                item = copy(event)
                item.pk = event.pk
                item.event_date = occurrence
                occurrences.append(item)
            if recurrence == 'NONE':
                break
            occurrence = _next_occurrence(event, occurrence)
    return sorted(occurrences, key=lambda item: item.event_date)


def _next_occurrence(event, occurrence):
    if event.recurrence == 'DAILY':
        return occurrence + timedelta(days=1)
    if event.recurrence == 'WEEKLY':
        return occurrence + timedelta(days=7)
    if event.recurrence == 'MONTHLY':
        month = occurrence.month + 1
        year = occurrence.year
        if month == 13:
            month = 1
            year += 1
        day = min(occurrence.day, calendar.monthrange(year, month)[1])
        return occurrence.replace(year=year, month=month, day=day)
    return occurrence


def calendar_bounds(year, month):
    start = timezone.datetime(year, month, 1, tzinfo=datetime_timezone.utc)
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    end = timezone.datetime(next_year, next_month, 1, tzinfo=datetime_timezone.utc)
    return start, end
