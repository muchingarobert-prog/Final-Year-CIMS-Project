from rest_framework import viewsets

from rest_framework.decorators import action

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response

from authentication.permissions import IsAdminUserRole

from .models import Notification

from .serializers import (
    NotificationSerializer
)


class NotificationViewSet(
    viewsets.ModelViewSet
):

    serializer_class = (
        NotificationSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUserRole()]

        return [IsAuthenticated()]

    def get_queryset(
        self
    ):

        return (
            Notification.objects.filter(
                recipient=self.request.user
            )
            .order_by(
                '-created_at'
            )
        )

    @action(
        detail=True,
        methods=['post']
    )
    def mark_read(
        self,
        request,
        pk=None
    ):

        notification = (
            self.get_object()
        )

        notification.is_read = True

        notification.save()

        return Response(
            {
                "message":
                "Notification marked as read"
            }
        )

    @action(
        detail=False,
        methods=['post']
    )
    def mark_all_read(
        self,
        request
    ):

        self.get_queryset().update(
            is_read=True
        )

        return Response(
            {
                "message":
                "All notifications marked as read"
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def unread(
        self,
        request
    ):

        notifications = (
            self.get_queryset().filter(
                is_read=False
            )
        )

        serializer = (
            NotificationSerializer(
                notifications,
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

        queryset = (
            self.get_queryset()
        )

        return Response(
            {
                "total":
                queryset.count(),

                "read":
                queryset.filter(
                    is_read=True
                ).count(),

                "unread":
                queryset.filter(
                    is_read=False
                ).count()
            }
        )