from rest_framework.routers import DefaultRouter

from .views import VisitorViewSet


router = DefaultRouter()

router.register(
    r'',
    VisitorViewSet,
    basename='visitors'
)

urlpatterns = router.urls