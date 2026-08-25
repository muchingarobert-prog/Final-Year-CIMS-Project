from django.db.models import Count

from rest_framework import viewsets

from rest_framework.decorators import action

from rest_framework.permissions import (
    IsAuthenticated,
    SAFE_METHODS,
)

from rest_framework.response import Response

from authentication.permissions import IsAdminUserRole

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

    queryset = (
        AttendanceSession.objects.all()
        .order_by('-session_date')
    )

    serializer_class = (
        AttendanceSessionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]

        if self.action in {'check_in'}:
            return [IsAuthenticated()]

        return [IsAdminUserRole()]

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

        total = (
            session.records.count()
        )

        present = (
            session.records.filter(
                status='PRESENT'
            ).count()
        )

        absent = (
            session.records.filter(
                status='ABSENT'
            ).count()
        )

        excused = (
            session.records.filter(
                status='EXCUSED'
            ).count()
        )

        attendance_rate = 0

        if total > 0:

            attendance_rate = round(
                (
                    present / total
                ) * 100,
                2
            )

        return Response(
            {
                "present":
                present,

                "absent":
                absent,

                "excused":
                excused,

                "attendance_rate":
                attendance_rate
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def leaderboard(
        self,
        request
    ):

        leaderboard = (

            AttendanceRecord.objects

            .filter(
                status='PRESENT'
            )

            .values(
                'member__id',
                'member__first_name',
                'member__last_name'
            )

            .annotate(
                total_attendance=Count(
                    'id'
                )
            )

            .order_by(
                '-total_attendance'
            )[:10]
        )

        return Response(
            leaderboard
        )


class AttendanceRecordViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        AttendanceRecord.objects.all()
    )

    serializer_class = (
        AttendanceRecordSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_permissions(self):
        if self.action in {'my_attendance', 'my_statistics'}:
            return [IsAuthenticated()]

        return [IsAdminUserRole()]

    @action(
        detail=False,
        methods=['get']
    )
    def my_attendance(
        self,
        request
    ):

        records = (
            AttendanceRecord.objects.filter(
                member=request.user
            )
        )

        serializer = (
            AttendanceRecordSerializer(
                records,
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
    def my_statistics(
        self,
        request
    ):

        total = (
            AttendanceRecord.objects.filter(
                member=request.user
            ).count()
        )

        present = (
            AttendanceRecord.objects.filter(
                member=request.user,
                status='PRESENT'
            ).count()
        )

        percentage = 0

        if total > 0:

            percentage = round(
                (
                    present / total
                ) * 100,
                2
            )

        return Response(
            {
                "total_records":
                total,

                "present":
                present,

                "attendance_percentage":
                percentage
            }
        )