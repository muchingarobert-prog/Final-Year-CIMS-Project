from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from church_members.models import User

from .serializers import (
    RegisterSerializer,
    UserSerializer,
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

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

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
            first_name__icontains=query
        ) | User.objects.filter(
            last_name__icontains=query
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

        return Response(
            {
                "username":
                    user.username,

                "email":
                    user.email,

                "role":
                    user.role,

                "committees":
                    user.committees.count(),
            }
        )