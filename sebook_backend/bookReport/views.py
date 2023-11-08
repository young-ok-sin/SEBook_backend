from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BookReport,User,Book
from .serializer import BookReportSerializer
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
class CreateBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum_report', openapi.IN_QUERY, description="userNum_report", type=openapi.TYPE_INTEGER),
        openapi.Parameter('reportContents', openapi.IN_QUERY, description="reportContents", type=openapi.TYPE_STRING),
        openapi.Parameter('reportTitle', openapi.IN_QUERY, description="reportTitle", type=openapi.TYPE_STRING),
        openapi.Parameter('isbn13_report', openapi.IN_QUERY, description="isbn13_report", type=openapi.TYPE_INTEGER)
    ])
    def post(self, request):
        userNum_report = request.query_params.get('userNum_report')
        reportContents = request.query_params.get('reportContents')
        reportTitle = request.query_params.get('reportTitle')
        isbn13_report = request.query_params.get('isbn13_report')
        
        user = User.objects.get(userNum=userNum_report)
        bookNum = Book.objects.get(isbn13=isbn13_report)
        
        book_report = BookReport.objects.create(
            userNum_report=user,
            reportContents=reportContents,
            reportTitle=reportTitle,
            isbn13_report=bookNum
        )
        
        # 생성된 BookReport 객체를 직렬화하여 응답 데이터로 반환
        serializer = BookReportSerializer(book_report)
        return JsonResponse(serializer.data)