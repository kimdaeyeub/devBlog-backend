from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    creator = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    categories = models.TextField()

    def __str__(self):
        return self.title
