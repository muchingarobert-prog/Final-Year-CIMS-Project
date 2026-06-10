from rest_framework import viewsets

from .models import (
    AttendanceSession,
    AttendanceRecord,
)

from .serializers import (
    AttendanceSessionSerializer,
    AttendanceRecordSerializer,
)


class AttendanceSessionViewSet(viewsets.ModelViewSet):

    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):

    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer