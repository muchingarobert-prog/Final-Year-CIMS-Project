from rest_framework import serializers

from .models import (
    Post,
    Comment,
    CommentReply,
    PostReaction,
    MediaGallery,
    PrayerRequest,
    Testimony,
)


class CommentReplySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = CommentReply

        fields = '__all__'


class CommentSerializer(
    serializers.ModelSerializer
):

    replies = CommentReplySerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Comment

        fields = '__all__'


class PostReactionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = PostReaction

        fields = '__all__'


class PostSerializer(
    serializers.ModelSerializer
):

    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    reactions = PostReactionSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Post

        fields = '__all__'


class MediaGallerySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = MediaGallery

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