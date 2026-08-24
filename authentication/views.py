from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import (
    urlsafe_base64_encode,
)

from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from church_members.models import User

from committees.models import CommitteeMembership
from notifications.models import Notification
from events.models import EventRegistration
from attendance.models import AttendanceRecord

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        return self.request.user


class SearchUsersView(generics.ListAPIView):

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        query = self.request.GET.get(
            "search",
            ""
        )

        return User.objects.filter(

            Q(first_name__icontains=query)

            |

            Q(last_name__icontains=query)

            |

            Q(username__icontains=query)

            |

            Q(email__icontains=query)

        )


class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        attendance_count = AttendanceRecord.objects.filter(
            member=user
        ).count()

        committee_count = CommitteeMembership.objects.filter(
            user=user,
            is_active=True
        ).count()

        event_count = EventRegistration.objects.filter(
            member=user
        ).count()

        unread_notifications = Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()

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

                    "attendance": attendance_count,

                    "committees": committee_count,

                    "events": event_count,

                    "unread_notifications":
                    unread_notifications

                }

            }

        )


class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        try:

            token = RefreshToken(
                request.data["refresh"]
            )

            token.blacklist()

            return Response(
                {
                    "message":
                    "Logout successful."
                }
            )

        except Exception:

            return Response(

                {
                    "message":
                    "Invalid refresh token."
                },

                status=status.HTTP_400_BAD_REQUEST

            )


class PasswordResetRequestView(APIView):

    serializer_class = PasswordResetRequestSerializer

    def post(self, request):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(

                {
                    "message":
                    "If that email exists, a reset link has been sent."
                }

            )

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = PasswordResetTokenGenerator().make_token(
            user
        )

        reset_link = (
            f"http://localhost:3000/reset-password/{uid}/{token}/"
        )

        send_mail(

            subject="Password Reset",

            message=f"Reset your password:\n\n{reset_link}",

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[email],

            fail_silently=False,

        )

        return Response(

            {
                "message":
                "Password reset email sent."
            }

        )


class PasswordResetConfirmView(APIView):

    serializer_class = PasswordResetConfirmSerializer

    def post(

        self,

        request,

        uidb64,

        token

    ):

        data = request.data.copy()

        data["uidb64"] = uidb64

        data["token"] = token

        serializer = self.serializer_class(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(

            {
                "message":
                "Password changed successfully."
            }

        )