from datetime import date

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get']
    )
    def search(self, request):

        query = request.GET.get(
            'q',
            ''
        )

        users = User.objects.filter(
            first_name__icontains=query
        ) | User.objects.filter(
            last_name__icontains=query
        ) | User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            email__icontains=query
        )

        serializer = UserSerializer(
            users.distinct(),
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def birthdays(self, request):

        today = date.today()

        users = User.objects.filter(
            date_of_birth__month=today.month
        ).order_by(
            'date_of_birth'
        )

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def dashboard(self, request):

        total_users = User.objects.count()

        male_members = User.objects.filter(
            gender='M'
        ).count()

        female_members = User.objects.filter(
            gender='F'
        ).count()

        active_committee_members = User.objects.filter(
            committees__isnull=False
        ).distinct().count()

        return Response(
            {
                'total_users': total_users,
                'male_members': male_members,
                'female_members': female_members,
                'committee_members': active_committee_members,
            }
        )