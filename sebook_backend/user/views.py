from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
#from rest_framework_simplejwt.tokens import RefreshToken

class GetUser(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum', None)
        if userNum is None:
            return Response({"error": "userNum parameter is required"}, status=400)

        try:
            user = User.objects.get(userNum=userNum)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

class UserSignUp(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userId', openapi.IN_QUERY, description="User id", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="User pw", type=openapi.TYPE_STRING)
    ])
    def post(self, request, *args, **kwargs):
        #swagger test
        # userId = request.GET.get('userId')
        # password = request.GET.get('password')
        
        userId = request.data.get('userId')
        password = request.data.get('password')

        userNum = User.authenticate_user(userId, password)
        if userNum is not None:
            return Response({"userNum": userNum}, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=401)

# class LogoutView(APIView):
#     def post(self, request, *args, **kwargs):
#         refresh_token = request.data.get('refreshToken')

#         if refresh_token:
#             try:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#                 return Response({"message": "Logout successful"}, status=200)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=400)
#         else:
#             return Response({"error": "Refresh token not provided"}, status=400)