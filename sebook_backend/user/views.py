from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
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