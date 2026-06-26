from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import (
    RefreshToken
)

from church_members.models import User

from committees.models import (
    CommitteeMembership
)

from notifications.models import (
    Notification
)

from events.models import (
    EventRegistration
)

from attendance.models import (
    AttendanceRecord
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
     ProfileSerializer,
)


class RegisterView(
    generics.CreateAPIView
):

    queryset = User.objects.all()

    serializer_class = (
        RegisterSerializer
    )


class ProfileView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = (
        ProfileSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(
        self
    ):

        return self.request.user

class SearchUsersView(
    generics.ListAPIView
):

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        query = self.request.GET.get(
            'search',
            ''
        )

        return User.objects.filter(
            Q(
                first_name__icontains=query
            ) |
            Q(
                last_name__icontains=query
            ) |
            Q(
                username__icontains=query
            ) |
            Q(
                email__icontains=query
            )
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

        user = request.user

        attendance_count = (
            AttendanceRecord.objects.filter(
                member=user
            ).count()
        )

        committee_count = (
            CommitteeMembership.objects.filter(
                user=user,
                is_active=True
            ).count()
        )

        event_count = (
            EventRegistration.objects.filter(
                member=user
            ).count()
        )

        unread_notifications = (
            Notification.objects.filter(
                recipient=user,
                is_read=False
            ).count()
        )

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role,
                },

                "statistics": {
                    "committees": committee_count,
                    "events": event_count,
                    "attendance": attendance_count,
                    "unread_notifications":
                    unread_notifications,
                }
            }
        )


class LogoutView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        try:

            refresh_token = request.data.get(
                'refresh'
            )

            token = RefreshToken(
                refresh_token
            )

            token.blacklist()

            return Response(
                {
                    "message":
                    "Logout successful"
                }
            )

        except Exception:

            return Response(
                {
                    "message":
                    "Invalid token"
                },
                status=400
            )