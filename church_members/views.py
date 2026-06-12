from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(
    viewsets.ModelViewSet
):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get']
    )
    def members(
        self,
        request
    ):

        members = User.objects.filter(
            role='MEMBER'
        )

        serializer = UserSerializer(
            members,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def leaders(
        self,
        request
    ):

        leaders = User.objects.exclude(
            role='MEMBER'
        )

        serializer = UserSerializer(
            leaders,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def birthdays(
        self,
        request
    ):

        users = User.objects.exclude(
            date_of_birth=None
        )

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data
        )