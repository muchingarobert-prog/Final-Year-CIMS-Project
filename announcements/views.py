from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(
    viewsets.ModelViewSet
):

    queryset = Announcement.objects.filter(
        is_active=True
    ).order_by(
        '-created_at'
    )

    serializer_class = (
        AnnouncementSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=['get']
    )
    def latest(
        self,
        request
    ):

        announcements = (
            Announcement.objects.filter(
                is_active=True
            )
            .order_by(
                '-created_at'
            )[:10]
        )

        serializer = (
            AnnouncementSerializer(
                announcements,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(
        self,
        request
    ):

        return Response(
            {
                "total":
                Announcement.objects.count(),

                "active":
                Announcement.objects.filter(
                    is_active=True
                ).count(),

                "committee_specific":
                Announcement.objects.filter(
                    target_type='COMMITTEE'
                ).count(),

                "general":
                Announcement.objects.filter(
                    target_type='ALL'
                ).count()
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def deactivate(
        self,
        request,
        pk=None
    ):

        announcement = (
            self.get_object()
        )

        announcement.is_active = False

        announcement.save()

        return Response(
            {
                "message":
                "Announcement deactivated"
            }
        )