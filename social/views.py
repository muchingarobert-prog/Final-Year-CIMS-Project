from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    
    Post,
    Comment,
    CommentReply,
    PostReaction,
    MediaGallery,
    PrayerRequest,
    Testimony,
)

from .serializers import (
    
    PostSerializer,
    CommentSerializer,
    CommentReplySerializer,
    PostReactionSerializer,
    MediaGallerySerializer,
    PrayerRequestSerializer,
    TestimonySerializer,
)


class PostViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        Post.objects.filter(
            is_active=True
        )
        .order_by(
            '-created_at'
        )
    )

    serializer_class = (
        PostSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=False,
        methods=['get']
    )
    def statistics(
        self,
        request
    ):

        return Response(
            {
                "posts":
                Post.objects.count(),

                "comments":
                Comment.objects.count(),

                "prayer_requests":
                PrayerRequest.objects.count(),

                "testimonies":
                Testimony.objects.count()
            }
        )

    @action(
        detail=True,
        methods=['post']
    )
    def deactivate(
        self,
        request,
        pk=None
    ):

        post = self.get_object()

        post.is_active = False

        post.save()

        return Response(
            {
                "message":
                "Post deactivated"
            }
        )


class CommentViewSet(
    viewsets.ModelViewSet
):

    queryset = Comment.objects.all()

    serializer_class = (
        CommentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class CommentReplyViewSet(
    viewsets.ModelViewSet
):

    queryset = CommentReply.objects.all()

    serializer_class = (
        CommentReplySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class PostReactionViewSet(
    viewsets.ModelViewSet
):

    queryset = PostReaction.objects.all()

    serializer_class = (
        PostReactionSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class MediaGalleryViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        MediaGallery.objects.all()
        .order_by('-uploaded_at')
    )

    serializer_class = (
        MediaGallerySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class PrayerRequestViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        PrayerRequest.objects.all()
        .order_by(
            '-created_at'
        )
    )

    serializer_class = (
        PrayerRequestSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=True,
        methods=['post']
    )
    def answered(
        self,
        request,
        pk=None
    ):

        prayer = self.get_object()

        prayer.is_answered = True

        prayer.save()

        return Response(
            {
                "message":
                "Prayer request marked answered"
            }
        )


class TestimonyViewSet(
    viewsets.ModelViewSet
):

    queryset = Testimony.objects.all()

    serializer_class = (
        TestimonySerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    @action(
        detail=True,
        methods=['post']
    )
    def approve(
        self,
        request,
        pk=None
    ):

        testimony = self.get_object()

        testimony.approved = True

        testimony.save()

        return Response(
            {
                "message":
                "Testimony approved"
            }
        )

    @action(
        detail=False,
        methods=['get']
    )
    def approved(
        self,
        request
    ):

        testimonies = (
            Testimony.objects.filter(
                approved=True
            )
        )

        serializer = (
            TestimonySerializer(
                testimonies,
                many=True
            )
        )

        return Response(
            serializer.data
        )