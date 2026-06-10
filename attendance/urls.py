from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceSessionViewSet,
    AttendanceRecordViewSet,
)

router = DefaultRouter()

router.register(
    'sessions',
    AttendanceSessionViewSet
)

router.register(
    'records',
    AttendanceRecordViewSet
)

urlpatterns = router.urls