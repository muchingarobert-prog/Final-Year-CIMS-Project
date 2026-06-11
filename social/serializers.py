from rest_framework import serializers

from .models import (
    Post,
    Comment,
    PrayerRequest,
    Testimony,
)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class PrayerRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrayerRequest
        fields = '__all__'


class TestimonySerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimony
        fields = '__all__'   