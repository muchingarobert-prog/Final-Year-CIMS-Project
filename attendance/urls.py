from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    AttendanceSessionViewSet,
    AttendanceRecordViewSet,
)

router = DefaultRouter()

router.register(
    r'sessions',
    AttendanceSessionViewSet
)

router.register(
    r'records',
    AttendanceRecordViewSet
)

urlpatterns = router.urls