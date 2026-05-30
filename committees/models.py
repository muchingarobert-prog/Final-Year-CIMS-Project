from django.db import models


class Committee(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    def __str__(self):
        return self.name