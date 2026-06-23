from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from attendance.models import (
    AttendanceRecord,
    AttendanceSession
)

from committees.models import (
    Committee,
    CommitteeMembership
)

from events.models import (
    Event,
    EventRegistration
)

from church_members.models import User


class ReportsView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        return JsonResponse(
            {
                "message":
                "Reports API"
            }
        )


class AttendanceReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        total_sessions = (
            AttendanceSession.objects.count()
        )

        total_records = (
            AttendanceRecord.objects.count()
        )

        total_present = (
            AttendanceRecord.objects.filter(
                status='PRESENT'
            ).count()
        )

        total_absent = (
            AttendanceRecord.objects.filter(
                status='ABSENT'
            ).count()
        )

        total_excused = (
            AttendanceRecord.objects.filter(
                status='EXCUSED'
            ).count()
        )

        attendance_rate = 0

        if total_records > 0:

            attendance_rate = round(
                (
                    total_present /
                    total_records
                ) * 100,
                2
            )

        return JsonResponse(
            {
                "total_sessions":
                total_sessions,

                "total_records":
                total_records,

                "present":
                total_present,

                "absent":
                total_absent,

                "excused":
                total_excused,

                "attendance_rate":
                attendance_rate
            }
        )


class CommitteeReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        committees = (
            Committee.objects.count()
        )

        memberships = (
            CommitteeMembership.objects.count()
        )

        active_committees = (
            Committee.objects.filter(
                is_active=True
            ).count()
        )

        return JsonResponse(
            {
                "committees":
                committees,

                "memberships":
                memberships,

                "active_committees":
                active_committees
            }
        )


class EventReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        total_events = (
            Event.objects.count()
        )

        registrations = (
            EventRegistration.objects.count()
        )

        upcoming_events = (
            Event.objects.filter(
                is_active=True
            ).count()
        )

        return JsonResponse(
            {
                "events":
                total_events,

                "registrations":
                registrations,

                "upcoming_events":
                upcoming_events
            }
        )


class MemberReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        total_members = (
            User.objects.count()
        )

        super_users = (
            User.objects.filter(
                role='SUPER_USER'
            ).count()
        )

        admin_users = (
            User.objects.filter(
                role='ADMIN_USER'
            ).count()
        )

        high_privilege = (
            User.objects.filter(
                role='HIGH_PRIVILEGE_USER'
            ).count()
        )

        members = (
            User.objects.filter(
                role='MEMBER'
            ).count()
        )

        return JsonResponse(
            {
                "total_members":
                total_members,

                "super_users":
                super_users,

                "admin_users":
                admin_users,

                "high_privilege_users":
                high_privilege,

                "members":
                members
            }
        )