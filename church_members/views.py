from datetime import date

from django.db.models import Q
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by(
        'first_name'
    )

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated
    ]

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
    def statistics(self, request):

        total_members = User.objects.count()

        male_count = User.objects.filter(
            gender='M'
        ).count()

        female_count = User.objects.filter(
            gender='F'
        ).count()

        members = User.objects.filter(
            role='MEMBER'
        ).count()

        admins = User.objects.exclude(
            role='MEMBER'
        ).count()

        return Response(
            {
                "total_members": total_members,
                "male_members": male_count,
                "female_members": female_count,
                "members": members,
                "administrators": admins,
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def committee_summary(self, request):

        data = []

        users = User.objects.prefetch_related(
            'committees'
        )

        for user in users:

            data.append(
                {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}",
                    "committee_count": user.committees.count()
                }
            )

        return Response(data)

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
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query)
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
    def role_breakdown(self, request):

        roles = (
            User.objects
            .values('role')
            .annotate(
                total=Count('id')
            )
            .order_by('role')
        )

        return Response(
            roles
        )

    @action(
        detail=False,
        methods=['get']
    )
    def recent_members(self, request):

        users = User.objects.order_by(
            '-date_joined'
        )[:20]

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data
        )