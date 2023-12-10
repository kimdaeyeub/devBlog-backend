# REST FRMAEWORK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT

# CUSTOM FILES
from .serializers import PostSerializer
from .models import Post


class GetAllPosts(APIView):
    def get(self, request):
        posts = Post.objects.filter()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class GetMyPosts(APIView):
    def get(self, request):
        posts = Post.objects.filter(creator=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class AddPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(
                creator=request.user,
            )
            return Response(PostSerializer(post).data)
        else:
            return Response(serializer.errors)


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = PostSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)

        if post.creator != request.user:
            return Response({"error": "You can't edit this post."})

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_post = serializer.save()
            return Response(PostSerializer(updated_post).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.creator != request.user:
            raise PermissionDenied
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)
