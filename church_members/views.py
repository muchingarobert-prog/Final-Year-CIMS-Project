from datetime import date

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=['get']
    )
    def birthdays(
        self,
        request
    ):

        today = date.today()

        users = User.objects.filter(
            date_of_birth__month=today.month
        ).order_by(
            'date_of_birth'
        )

        data = []

        for user in users:

            data.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_of_birth": user.date_of_birth,
                }
            )

        return Response(data)