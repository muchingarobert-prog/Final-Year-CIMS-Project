from django.db.models import Sum

from rest_framework import viewsets

from rest_framework.decorators import action

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response

from .models import (
    FinancialCategory,
    Income,
    Expense,
)

from .serializers import (
    FinancialCategorySerializer,
    IncomeSerializer,
    ExpenseSerializer,
)


class FinancialCategoryViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        FinancialCategory.objects.all()
    )

    serializer_class = (
        FinancialCategorySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class IncomeViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        Income.objects.all()
        .order_by('-created_at')
    )

    serializer_class = (
        IncomeSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            recorded_by=self.request.user
        )

    @action(
        detail=False,
        methods=['get']
    )
    def summary(
        self,
        request
    ):

        total_income = (
            Income.objects.aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        return Response(
            {
                "total_income":
                total_income
            }
        )


class ExpenseViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        Expense.objects.all()
        .order_by('-created_at')
    )

    serializer_class = (
        ExpenseSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer
    ):

        serializer.save(
            requested_by=self.request.user
        )

    @action(
        detail=True,
        methods=['post']
    )
    def approve(
        self,
        request,
        pk=None
    ):

        expense = self.get_object()

        expense.status = 'APPROVED'

        expense.approved_by = (
            request.user
        )

        expense.save()

        return Response(
            {
                "message":
                "Expense approved"
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def summary(
        self,
        request
    ):

        total_expenses = (
            Expense.objects.filter(
                status='APPROVED'
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )

        return Response(
            {
                "total_expenses":
                total_expenses
            }
        )