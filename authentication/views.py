from rest_framework import generics

from rest_framework.permissions import (
    IsAuthenticated
)

from church_members.models import User

from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
)


class RegisterView(
    generics.CreateAPIView
):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


class ProfileView(
    generics.RetrieveUpdateAPIView
):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        return self.request.user