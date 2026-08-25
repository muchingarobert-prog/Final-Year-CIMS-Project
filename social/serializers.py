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


class CommentReplySerializer(serializers.ModelSerializer):

    author_name = serializers.SerializerMethodField()

    class Meta:

        model = CommentReply

        fields = [
            "id",
            "comment",
            "author",
            "author_name",
            "content",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "author_name",
            "created_at",
        ]

    def get_author_name(self, obj):

        return (
            f"{obj.author.first_name} "
            f"{obj.author.last_name}"
        ).strip()


class CommentSerializer(serializers.ModelSerializer):

    author_name = serializers.SerializerMethodField()

    reply_count = serializers.SerializerMethodField()

    replies = CommentReplySerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Comment

        fields = [
            "id",
            "post",
            "author",
            "author_name",
            "content",
            "reply_count",
            "replies",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "author",
            "author_name",
            "created_at",
        ]

    def get_author_name(self, obj):

        return (
            f"{obj.author.first_name} "
            f"{obj.author.last_name}"
        ).strip()

    def get_reply_count(self, obj):

        return obj.replies.count()


class PostReactionSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()

    class Meta:

        model = PostReaction

        fields = [
            "id",
            "post",
            "user",
            "user_name",
            "reaction_type",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "user_name",
            "created_at",
        ]

    def get_user_name(self, obj):

        return (
            f"{obj.user.first_name} "
            f"{obj.user.last_name}"
        ).strip()


class PostSerializer(serializers.ModelSerializer):

    author_name = serializers.SerializerMethodField()

    comment_count = serializers.SerializerMethodField()

    reaction_count = serializers.SerializerMethodField()

    like_count = serializers.SerializerMethodField()

    love_count = serializers.SerializerMethodField()

    amen_count = serializers.SerializerMethodField()

    pray_count = serializers.SerializerMethodField()

    my_reaction = serializers.SerializerMethodField()

    is_owner = serializers.SerializerMethodField()

    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Post

        fields = [
            "id",
            "title",
            "content",
            "author",
            "author_name",
            "privacy",
            "is_active",
            "created_at",
            "updated_at",
            "comment_count",
            "reaction_count",
            "like_count",
            "love_count",
            "amen_count",
            "pray_count",
            "my_reaction",
            "is_owner",
            "comments",
        ]

        read_only_fields = [
            "id",
            "author",
            "author_name",
            "created_at",
            "updated_at",
            "comment_count",
            "reaction_count",
            "like_count",
            "love_count",
            "amen_count",
            "pray_count",
            "my_reaction",
            "is_owner",
            "comments",
        ]

    def get_author_name(self, obj):

        return (
            f"{obj.author.first_name} "
            f"{obj.author.last_name}"
        ).strip()

    def get_comment_count(self, obj):

        return obj.comments.count()

    def get_reaction_count(self, obj):

        return obj.reactions.count()

    def get_like_count(self, obj):

        return obj.reactions.filter(
            reaction_type="LIKE"
        ).count()

    def get_love_count(self, obj):

        return obj.reactions.filter(
            reaction_type="LOVE"
        ).count()

    def get_amen_count(self, obj):

        return obj.reactions.filter(
            reaction_type="AMEN"
        ).count()

    def get_pray_count(self, obj):

        return obj.reactions.filter(
            reaction_type="PRAY"
        ).count()

    def get_my_reaction(self, obj):

        request = self.context.get(
            "request"
        )

        if not request:

            return None

        reaction = obj.reactions.filter(
            user=request.user
        ).first()

        if reaction:

            return reaction.reaction_type

        return None

    def get_is_owner(self, obj):

        request = self.context.get(
            "request"
        )

        if not request:

            return False

        return obj.author == request.user


class MediaGallerySerializer(serializers.ModelSerializer):

    uploader_name = serializers.SerializerMethodField()

    class Meta:

        model = MediaGallery

        fields = [
            "id",
            "title",
            "file",
            "uploaded_by",
            "uploader_name",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "uploaded_by",
            "uploader_name",
            "uploaded_at",
        ]

    def get_uploader_name(self, obj):

        return (
            f"{obj.uploaded_by.first_name} "
            f"{obj.uploaded_by.last_name}"
        ).strip()


class PrayerRequestSerializer(serializers.ModelSerializer):

    member_name = serializers.SerializerMethodField()

    class Meta:

        model = PrayerRequest

        fields = [
            "id",
            "title",
            "request",
            "member",
            "member_name",
            "is_answered",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "member",
            "member_name",
            "created_at",
            "is_answered",
        ]

    def get_member_name(self, obj):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        ).strip()


class TestimonySerializer(serializers.ModelSerializer):

    member_name = serializers.SerializerMethodField()

    class Meta:

        model = Testimony

        fields = [
            "id",
            "title",
            "content",
            "member",
            "member_name",
            "approved",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "member",
            "member_name",
            "approved",
            "created_at",
        ]

    def get_member_name(self, obj):

        return (
            f"{obj.member.first_name} "
            f"{obj.member.last_name}"
        ).strip()