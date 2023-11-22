from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.contrib.auth import authenticate,login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import logout
#from rest_framework_simplejwt.tokens import RefreshToken

class GetUser(APIView):
    def get(self, request):
        try:
            user = request.user
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class UserSignUp(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'userId': openapi.Schema(type=openapi.TYPE_STRING, description='userId'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
        }
    ))
    def post(self, request):
        userId = request.data.get('userId')
        password = request.data.get('password')
        name = request.data.get('name')

        if userId is None or password is None or name is None: 
            return Response({"error": "userId, password and name are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 커스텀 User 모델에 맞게 사용자 생성
        user = CustomUser.objects.create_user(userId=userId, name=name)
        user.set_password(password)  # 비밀번호를 암호화하여 저장
        user.save()


        return Response({"message": "User created", "userId": user.userId}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="User id", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="User pw", type=openapi.TYPE_STRING)
    ])
    def post(self, request, *args, **kwargs):
        #username = request.query_params.get('username')
        #password = request.query_params.get('password')
        username = request.data.get('username')
        password = request.data.get('password')

        print("id",username)
        print("pw",password)
        print(request.user)
        if not username or not password:
            return Response({"error": "Invalid credentials"}, status=401)

        user = authenticate(request, userId=username, password=password)

        print("user",user)

        if user is not None:
            login(request, user)
            print(request.session)

            print("rrrrrr",user.userNum)
            return Response({
                "userNum": user.userNum,
                "userName": user.name
            }, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=401)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=200)
