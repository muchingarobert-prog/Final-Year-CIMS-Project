from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Post,
    Comment,
    PrayerRequest,
    Testimony,
)

from .serializers import (
    PostSerializer,
    CommentSerializer,
    PrayerRequestSerializer,
    TestimonySerializer,
)


class PostViewSet(
    viewsets.ModelViewSet
):

    queryset = Post.objects.all().order_by(
        '-created_at'
    )

    serializer_class = PostSerializer

    permission_classes = [
        IsAuthenticated
    ]


class CommentViewSet(
    viewsets.ModelViewSet
):

    queryset = Comment.objects.all()

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticated
    ]


class PrayerRequestViewSet(
    viewsets.ModelViewSet
):

    queryset = PrayerRequest.objects.all().order_by(
        '-created_at'
    )

    serializer_class = PrayerRequestSerializer

    permission_classes = [
        IsAuthenticated
    ]


class TestimonyViewSet(
    viewsets.ModelViewSet
):

    queryset = Testimony.objects.all()

    serializer_class = TestimonySerializer

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