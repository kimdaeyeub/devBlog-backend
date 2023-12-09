from rest_framework import serializers
from .models import Post
from users.serializers import PublicUserSerializer


class PostSerializer(serializers.ModelSerializer):
    creator = PublicUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Post
        fields = "__all__"
