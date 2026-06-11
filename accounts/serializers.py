from rest_framework import serializers
from church_members.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'phone_number',
        ]