from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .serializers import PrivateUserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated


# NOTE: 회원가입을 하기 위해서는 username,name,password가 필요하다.
class Join(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("password required")
        serializers = PrivateUserSerializer(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            user.set_password(password)
            user.save()
            serializers = PrivateUserSerializer(user)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("username and password required")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Success"})
        else:
            return Response({"message": "Invalid credentials"})


class GetMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user:
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"message": "Invalid credentials"})

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LogOut(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Success"})
