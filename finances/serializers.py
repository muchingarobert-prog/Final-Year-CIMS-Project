from rest_framework import serializers

from .models import (
    FinancialCategory,
    Income,
    Expense,
)


class FinancialCategorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = FinancialCategory

        fields = '__all__'


class IncomeSerializer(
    serializers.ModelSerializer
):

    member_name = serializers.SerializerMethodField()

    class Meta:

        model = Income

        fields = '__all__'

    def get_member_name(
        self,
        obj
    ):

        if not obj.member:
            return None

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        )


class ExpenseSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Expense

        fields = '__all__'

        read_only_fields = [
            'id',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'recorded_by',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'status',
            'requested_by',
            'approved_by',
            'created_at',
            'updated_at',
        ]