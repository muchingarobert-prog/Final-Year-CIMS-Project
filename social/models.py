from django.db import models
from django.conf import settings


class Post(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author} - {self.post}"


class CommentReply(models.Model):

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Reply by {self.author}"


class PostReaction(models.Model):

    REACTION_CHOICES = [
        ('LIKE', 'Like'),
        ('LOVE', 'Love'),
        ('AMEN', 'Amen'),
        ('PRAY', 'Pray'),
    ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reactions'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    reaction_type = models.CharField(
        max_length=20,
        choices=REACTION_CHOICES,
        default='LIKE'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'post',
            'user'
        )

    def __str__(self):
        return f"{self.user} - {self.reaction_type}"


class MediaGallery(models.Model):

    title = models.CharField(
        max_length=200
    )

    file = models.FileField(
        upload_to='gallery/'
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class PrayerRequest(models.Model):

    title = models.CharField(
        max_length=200
    )

    request = models.TextField()

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    is_answered = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Testimony(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title