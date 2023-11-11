from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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