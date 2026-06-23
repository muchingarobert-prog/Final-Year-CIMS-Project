from django.utils import timezone

from django.db.models import Count

from rest_framework.views import APIView

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import (
    Response
)

from church_members.models import (
    User
)

from committees.models import (
    Committee
)

from attendance.models import (
    AttendanceSession,
    AttendanceRecord
)

from events.models import (
    Event,
    EventRegistration
)

from notifications.models import (
    Notification
)


class DashboardView(
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

        unread_notifications = (
            Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).count()
        )

        upcoming_events = (
            Event.objects.filter(
                start_date__gte=timezone.now()
            ).count()
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

                "upcoming_events":
                upcoming_events,

                "unread_notifications":
                unread_notifications
            }
        )


class DashboardAnalyticsView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        top_attendees = (
            AttendanceRecord.objects
            .filter(
                status='PRESENT'
            )
            .values(
                'member__first_name',
                'member__last_name'
            )
            .annotate(
                attendance_count=Count(
                    'id'
                )
            )
            .order_by(
                '-attendance_count'
            )[:10]
        )

        top_events = (
            Event.objects
            .annotate(
                registration_count=Count(
                    'registrations'
                )
            )
            .order_by(
                '-registration_count'
            )[:10]
        )

        event_data = []

        for event in top_events:

            event_data.append(
                {
                    "id":
                    event.id,

                    "title":
                    event.title,

                    "registrations":
                    event.registration_count
                }
            )

        return Response(
            {
                "top_attendees":
                list(top_attendees),

                "top_events":
                event_data
            }
        )