from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Community,User,Book
from .serializer import CommunitySerializer
from rest_framework.response import Response
from django.http import JsonResponse

class CreateParagraph(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('contents', openapi.IN_QUERY, description="Paragraph", type=openapi.TYPE_STRING),
        openapi.Parameter('userNum_community', openapi.IN_QUERY, description="userNum_community", type=openapi.TYPE_INTEGER),
        openapi.Parameter('isbn13_community', openapi.IN_QUERY, description="isbn13_community", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        contents = request.data.get('contents')
        userNum_community = request.data.get('userNum_community')
        isbn13_community = request.data.get('isbn13_community')
        
        # User 모델과 Book 모델의 인스턴스 가져오기
        user = User.objects.get(userNum=userNum_community)
        book = Book.objects.get(isbn13=isbn13_community)
        
        community = Community.objects.create(
            contents=contents,
            userNum_community=user,
            isbn13_community=book
        )
        
        # 생성된 Community 객체를 직렬화하여 응답 데이터로 반환
        serializer = CommunitySerializer(community)
        return JsonResponse(serializer.data)

class CommunityListRead(APIView):
    def get(self, request):
        community_list =  Community.objects.all()

        if not community_list:
            return Response({"message": "No Community found"}, status=404)

        serializer = CommunitySerializer(community_list, many=True)
        return Response({"CommunityList": serializer.data})