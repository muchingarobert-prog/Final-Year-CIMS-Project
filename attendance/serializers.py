from rest_framework import serializers

from .models import (
    AttendanceSession,
    AttendanceRecord,
)


class AttendanceRecordSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.SerializerMethodField()

    class Meta:

        model = AttendanceRecord

        fields = [
            'id',
            'member',
            'member_name',
            'session',
            'status',
            'remarks',
            'recorded_at',
        ]

        read_only_fields = [
            'id',
            'member_name',
            'recorded_at',
        ]

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        request = self.context.get('request')

        if not request or request.user.role not in [
            'SUPER_USER',
            'ADMIN_USER',
            'HIGH_PRIVILEGE_USER'
        ]:
            extra_kwargs['member'] = {'read_only': True}

        return extra_kwargs

    def get_member_name(
        self,
        obj
    ):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )


class AttendanceSessionSerializer(
    serializers.ModelSerializer
):

    total_present = (
        serializers.SerializerMethodField()
    )

    total_absent = (
        serializers.SerializerMethodField()
    )

    total_excused = (
        serializers.SerializerMethodField()
    )

    attendance_rate = (
        serializers.SerializerMethodField()
    )

    class Meta:

        model = AttendanceSession

        fields = [
            'id',
            'title',
            'service_type',
            'session_date',
            'notes',
            'is_active',
            'total_present',
            'total_absent',
            'total_excused',
            'attendance_rate',
        ]

    def get_total_present(
        self,
        obj
    ):

        return obj.records.filter(
            status='PRESENT'
        ).count()

    def get_total_absent(
        self,
        obj
    ):

        return obj.records.filter(
            status='ABSENT'
        ).count()

    def get_total_excused(
        self,
        obj
    ):

        return obj.records.filter(
            status='EXCUSED'
        ).count()

    def get_attendance_rate(
        self,
        obj
    ):

        total = obj.records.count()

        if total == 0:
            return 0

        present = obj.records.filter(
            status='PRESENT'
        ).count()

        return round(
            (
                present / total
            ) * 100,
            2
        )