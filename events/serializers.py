from rest_framework import serializers

from .models import (
    Event,
    EventRegistration,
)


class EventSerializer(
    serializers.ModelSerializer
):

    event_date = serializers.DateTimeField(
        input_formats=[
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d',
        ]
    )

    recurrence_end_date = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%Y-%m-%d'],
    )

    weekday = serializers.SerializerMethodField()

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
            'weekday',
            'event_date',
            'location',
            'registration_required',
            'max_attendees',
            'recurrence',
            'recurrence_day',
            'recurrence_end_date',
            'attendee_count',
            'available_slots',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]


    def to_internal_value(self, data):
        data = data.copy()
        if 'recurrence_end_date' in data and data['recurrence_end_date'] == '':
            data['recurrence_end_date'] = None
        return super().to_internal_value(data)

    def get_weekday(
        self,
        obj
    ):

        if not obj.event_date:
            return None

        return obj.event_date.strftime('%A')

    def get_attendee_count(
        self,
        obj
    ):

        return obj.registrations.count()

    def validate(
        self,
        attrs
    ):

        recurrence = attrs.get(
            'recurrence',
            getattr(self.instance, 'recurrence', 'NONE')
        )

        recurrence_day = attrs.get(
            'recurrence_day',
            getattr(self.instance, 'recurrence_day', '')
        )

        if recurrence == 'WEEKLY' and not recurrence_day:
            raise serializers.ValidationError(
                {
                    'recurrence_day':
                    'recurrence_day is required for weekly recurring events.'
                }
            )

        if recurrence != 'WEEKLY' and recurrence_day:
            raise serializers.ValidationError(
                {
                    'recurrence_day':
                    'recurrence_day should only be set for weekly recurring events.'
                }
            )

        if recurrence == 'NONE' and attrs.get('recurrence_end_date'):
            raise serializers.ValidationError(
                {
                    'recurrence_end_date':
                    'recurrence_end_date should be empty unless recurrence is set.'
                }
            )

        return attrs

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

        read_only_fields = [
            'id',
            'member',
            'member_name',
            'registration_date',
        ]

    def get_member_name(
        self,
        obj
    ):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )