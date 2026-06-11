from rest_framework import viewsets

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


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PrayerRequestViewSet(viewsets.ModelViewSet):

    queryset = PrayerRequest.objects.all()
    serializer_class = PrayerRequestSerializer


class TestimonyViewSet(viewsets.ModelViewSet):

    queryset = Testimony.objects.all()
    serializer_class = TestimonySerializer  