from rest_framework import serializers

from .models import User


class UserSerializer(
    serializers.ModelSerializer
):

    committees = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:

        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'gender',
            'phone_number',
            'date_of_birth',
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
            'committees',
        ]