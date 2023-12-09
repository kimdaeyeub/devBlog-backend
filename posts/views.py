from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import PostSerializer
from .models import Post
from rest_framework.exceptions import NotFound


class GetAllPosts(APIView):
    def get(self, request):
        posts = Post.objects.filter(creator=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class AddPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.save(
                creator=request.user,
            )
            return Response(PostSerializer(serializer).data)
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
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
