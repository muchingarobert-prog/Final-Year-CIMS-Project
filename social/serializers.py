from rest_framework import serializers

from .models import (
    Post,
    Comment,
    PrayerRequest,
    Testimony,
)


class CommentSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Comment

        fields = '__all__'


class PostSerializer(
    serializers.ModelSerializer
):

    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Post

        fields = '__all__'


class PrayerRequestSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PrayerRequest

        fields = '__all__'


class TestimonySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Testimony

        fields = '__all__'