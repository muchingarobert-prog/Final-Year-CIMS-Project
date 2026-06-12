from rest_framework import serializers

from .models import (
    Event,
    EventRegistration,
)


class EventSerializer(
    serializers.ModelSerializer
):

    attendee_count = serializers.SerializerMethodField()

    class Meta:

        model = Event

        fields = [
            'id',
            'title',
            'description',
            'event_type',
            'start_date',
            'end_date',
            'location',
            'registration_required',
            'max_attendees',
            'attendee_count',
            'is_active',
        ]

    def get_attendee_count(
        self,
        obj
    ):
        return obj.registrations.count()


class EventRegistrationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = EventRegistration

        fields = '__all__'