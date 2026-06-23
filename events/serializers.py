from rest_framework import serializers

from .models import (
    Event,
    EventRegistration,
)


class EventRegistrationSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.SerializerMethodField()

    class Meta:

        model = EventRegistration

        fields = [
            'id',
            'event',
            'member',
            'member_name',
            'registration_date',
            'status',
        ]

    def get_member_name(
        self,
        obj
    ):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )


class EventSerializer(
    serializers.ModelSerializer
):

    attendee_count = (
        serializers.SerializerMethodField()
    )

    available_slots = (
        serializers.SerializerMethodField()
    )

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
            'available_slots',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_attendee_count(
        self,
        obj
    ):

        return obj.registrations.count()

    def get_available_slots(
        self,
        obj
    ):

        if not obj.max_attendees:

            return None

        return (
            obj.max_attendees -
            obj.registrations.count()
        )