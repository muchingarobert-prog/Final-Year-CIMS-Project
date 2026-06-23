from django.db.models import Count
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response

from church_members.models import User

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

from finances.models import (
    Income,
    Expense
)


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

        total_members = (
            User.objects.count()
        )

        total_committees = (
            Committee.objects.count()
        )

        total_events = (
            Event.objects.count()
        )

        total_sessions = (
            AttendanceSession.objects.count()
        )

        return Response(
            {
                "members":
                total_members,

                "committees":
                total_committees,

                "events":
                total_events,

                "attendance_sessions":
                total_sessions,
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

        total_records = (
            AttendanceRecord.objects.count()
        )

        present = (
            AttendanceRecord.objects.filter(
                status='PRESENT'
            ).count()
        )

        absent = (
            AttendanceRecord.objects.filter(
                status='ABSENT'
            ).count()
        )

        excused = (
            AttendanceRecord.objects.filter(
                status='EXCUSED'
            ).count()
        )

        return Response(
            {
                "total_records":
                total_records,

                "present":
                present,

                "absent":
                absent,

                "excused":
                excused,
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
            Committee.objects.annotate(
                total_members=Count(
                    'memberships'
                )
            )
        )

        data = []

        for committee in committees:

            data.append(
                {
                    "id":
                    committee.id,

                    "name":
                    committee.name,

                    "members":
                    committee.total_members,
                }
            )

        return Response(
            data
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

        total_registrations = (
            EventRegistration.objects.count()
        )

        return Response(
            {
                "events":
                total_events,

                "registrations":
                total_registrations,
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

        male_members = (
            User.objects.filter(
                gender='M'
            ).count()
        )

        female_members = (
            User.objects.filter(
                gender='F'
            ).count()
        )

        return Response(
            {
                "total_members":
                total_members,

                "male_members":
                male_members,

                "female_members":
                female_members,
            }
        )


class FinanceReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        total_income = (
            Income.objects.aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        total_expenses = (
            Expense.objects.filter(
                status='APPROVED'
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        balance = (
            total_income -
            total_expenses
        )

        return Response(
            {
                "income":
                total_income,

                "expenses":
                total_expenses,

                "balance":
                balance,
            }
        )