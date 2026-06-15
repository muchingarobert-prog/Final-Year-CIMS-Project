from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    AttendanceSession,
    AttendanceRecord,
)

from .serializers import (
    AttendanceSessionSerializer,
    AttendanceRecordSerializer,
)


class AttendanceSessionViewSet(
    viewsets.ModelViewSet
):

    queryset = AttendanceSession.objects.all().order_by(
        '-session_date'
    )

    serializer_class = (
        AttendanceSessionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=True,
        methods=['post']
    )
    def check_in(
        self,
        request,
        pk=None
    ):

        session = self.get_object()

        record, created = (
            AttendanceRecord.objects.get_or_create(
                member=request.user,
                session=session,
                defaults={
                    'status': 'PRESENT'
                }
            )
        )

        if not created:

            return Response(
                {
                    "message":
                    "Attendance already recorded"
                }
            )

        return Response(
            {
                "message":
                "Attendance recorded"
            }
        )

    @action(
        detail=True,
        methods=['get']
    )
    def statistics(
        self,
        request,
        pk=None
    ):

        session = self.get_object()

        return Response(
            {
                "present":
                session.records.filter(
                    status='PRESENT'
                ).count(),

                "absent":
                session.records.filter(
                    status='ABSENT'
                ).count(),

                "excused":
                session.records.filter(
                    status='EXCUSED'
                ).count(),
            }
        )


class AttendanceRecordViewSet(
    viewsets.ModelViewSet
):

    queryset = AttendanceRecord.objects.all()

    serializer_class = (
        AttendanceRecordSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]