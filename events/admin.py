from django.contrib import admin
from .models import Event, EventRegistration


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

    


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'event',
        'status',
        'registration_date',
    )

    list_filter = (
        'status',
        'event',
    )

    search_fields = (
        'member__first_name',
        'member__last_name',
        'event__title',
    )

    ordering = (
        '-registration_date',
    )