from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'event_type',
        'start_date',
        'end_date',
        'location',
        'registration_required',
    )

    list_filter = (
        'event_type',
        'registration_required',
        'start_date',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    ordering = (
        '-start_date',
    )

    filter_horizontal = (
        'attendees',
    )