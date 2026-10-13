from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import IsHighPrivilegeOrAbove, user_has_any_role

from django.db.models import Q

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

    def get_permissions(self):
        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy',
            'deactivate',
        ]:
            return [IsHighPrivilegeOrAbove()]

        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Announcement.objects.filter(
            is_active=True
        ).order_by(
            '-created_at'
        )

        if user_has_any_role(self.request.user, ['SUPER_USER', 'ADMIN_USER', 'HIGH_PRIVILEGE_USER']):
            return queryset

        return queryset.filter(
            Q(target_type='ALL') |
            Q(
                target_type='COMMITTEE',
                committee__memberships__user=self.request.user,
                committee__memberships__is_active=True,
            )
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(
        detail=False,
        methods=['get']
    )
    def latest(
        self,
        request
    ):

        announcements = self.get_queryset()[:10]

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
                self.get_queryset().count(),

                "active":
                self.get_queryset().count(),

                "committee_specific":
                self.get_queryset().filter(
                    target_type='COMMITTEE'
                ).count(),

                "general":
                self.get_queryset().filter(
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