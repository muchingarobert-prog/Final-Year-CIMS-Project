from rest_framework import serializers

from .models import User


class BirthdaySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = User

        fields = [
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'profile_picture',
        ]