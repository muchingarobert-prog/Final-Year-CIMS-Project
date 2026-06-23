from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Visitor
from .serializers import VisitorSerializer


class VisitorViewSet(
    viewsets.ModelViewSet
):

    queryset = Visitor.objects.all().order_by(
        '-visit_date'
    )

    serializer_class = VisitorSerializer

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(
        self,
        request
    ):

        total = Visitor.objects.count()

        pending = Visitor.objects.filter(
            follow_up_status='PENDING'
        ).count()

        joined = Visitor.objects.filter(
            follow_up_status='JOINED'
        ).count()

        return Response(
            {
                "total_visitors": total,
                "pending_followups": pending,
                "joined_members": joined,
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def status_breakdown(
        self,
        request
    ):

        data = (
            Visitor.objects
            .values('follow_up_status')
            .annotate(
                total=Count('id')
            )
        )

        return Response(data)