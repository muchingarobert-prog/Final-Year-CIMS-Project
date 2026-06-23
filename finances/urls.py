from rest_framework.routers import (
    DefaultRouter
)

from .views import (
    FinancialCategoryViewSet,
    IncomeViewSet,
    ExpenseViewSet,
)

router = DefaultRouter()

router.register(
    r'categories',
    FinancialCategoryViewSet
)

router.register(
    r'income',
    IncomeViewSet
)

router.register(
    r'expenses',
    ExpenseViewSet
)

urlpatterns = router.urls