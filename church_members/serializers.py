from datetime import date

from rest_framework import serializers

from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(
    serializers.ModelSerializer
):

    committees = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    full_name = serializers.SerializerMethodField()

    age = serializers.SerializerMethodField()

    committee_count = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'role',
            'gender',
            'phone_number',
            'date_of_birth',
            'age',
            'date_of_baptism',
            'date_of_sealing',
            'residential_address',
            'residential_apostle_area',
            'school_residential_address',
            'programme_of_study',
            'year_of_study',
            'profile_picture',
            'bio',
            'church_role_description',
            'interests_and_skills',
            'is_profile_public',
            'receive_notifications',
            'committee_count',
            'committees',
        ]

    def get_full_name(
        self,
        obj
    ):

        return (
            f"{obj.first_name} "
            f"{obj.last_name}"
        ).strip()

    def get_committee_count(
        self,
        obj
    ):

        return obj.committees.count()

    def get_age(
        self,
        obj
    ):

        if not obj.date_of_birth:
            return None

        today = date.today()

        return (
            today.year -
            obj.date_of_birth.year -
            (
                (
                    today.month,
                    today.day
                ) <
                (
                    obj.date_of_birth.month,
                    obj.date_of_birth.day
                )
            )
        )

    def validate(self, attrs):
        request = self.context.get('request')

        if not request or not request.user or not request.user.is_authenticated:
            return attrs

        restricted_fields = ['role', 'is_staff', 'is_superuser', 'is_active']
        if not request.user.is_superuser and any(field in attrs for field in restricted_fields):
            raise ValidationError(
                'You are not allowed to change administrative account settings.'
            )

        return attrs