from django import forms
from django.contrib import admin
from .models import Event, EventRegistration


class EventAdminForm(forms.ModelForm):
    event_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'text'},
        ),
        input_date_formats=[
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M',
        ],
        input_time_formats=[
            '%H:%M',
            '%H:%Mhrs',
            '%H:%M hrs',
            '%H:%M:%S',
            '%I:%M %p',
        ],
    )

    class Meta:
        model = Event
        exclude = ('created_by',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    list_display = (
        'title',
        'event_type',
        'recurrence',
        'recurrence_day',
        'event_date',
        'location',
        'registration_required',
    )

    list_filter = (
        'event_type',
        'recurrence',
        'registration_required',
        'event_date',
    )

    search_fields = (
        'title',
        'description',
        'location',
    )

    ordering = (
        '-event_date',
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