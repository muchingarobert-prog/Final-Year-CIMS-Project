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