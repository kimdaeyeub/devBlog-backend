from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=100,
        editable=False,
    )
    last_name = models.CharField(
        max_length=100,
        editable=False,
    )

    name = models.CharField(
        max_length=100,
    )

    avatar = models.URLField(
        blank=True,
    )
