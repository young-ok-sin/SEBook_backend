from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BookReport,User,Book,LikeBookReport
from .serializer import BookReportSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

# Create your views here.
class CreateBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum_report', openapi.IN_QUERY, description="userNum_report", type=openapi.TYPE_INTEGER),
        openapi.Parameter('reportContents', openapi.IN_QUERY, description="reportContents", type=openapi.TYPE_STRING),
        openapi.Parameter('reportTitle', openapi.IN_QUERY, description="reportTitle", type=openapi.TYPE_STRING),
        openapi.Parameter('isbn13_report', openapi.IN_QUERY, description="isbn13_report", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        userNum_report = request.data.get('userNum_report')
        reportContents = request.data.get('reportContents')
        reportTitle = request.data.get('reportTitle')
        isbn13_report = request.data.get('isbn13_report')
        
        try:
            user = User.objects.get(userNum=userNum_report)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)
        try:
            book = Book.objects.get(isbn13=isbn13_report)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist."}, status=404)
        
        book_report = BookReport.objects.create(
            userNum_report=user,
            reportContents=reportContents,
            reportTitle=reportTitle,
            isbn13_report=book
        )
        
        # 생성된 BookReport 객체를 직렬화하여 응답 데이터로 반환
        serializer = BookReportSerializer(book_report)
        return JsonResponse(serializer.data)

class DeleteBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('reportNum', openapi.IN_QUERY, description="reportNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request):
        book_report_num = request.query_params
        try:
            book_report = BookReport.objects.get(reportNum=book_report_num['reportNum'])
        except BookReport.DoesNotExist:
            return Response({"error": "BookReport not found"}, status=status.HTTP_404_NOT_FOUND)
        book_report.delete()
        return Response({"message": "BookReport deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class UserSavedBookReports(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum')
        
        try:
            user = User.objects.get(userNum=userNum)
            like_bookreports = LikeBookReport.objects.filter(userNum_like_bookreport=user)
            saved_books = [like_bookreport.reportNum_like_bookreport for like_bookreport in like_bookreports]
            serializer = BookReportSerializer(saved_books, many=True)
            return Response({"likeBookReportList": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UserWriteBookReports(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum')
        
        try:
            user = User.objects.get(userNum=userNum)
            bookreports = BookReport.objects.filter(userNum_report=user)
            serializer = BookReportSerializer(bookreports, many=True)
            return Response({"userWriteBookReportList": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class ReadAllBookReport(APIView):
    def get(self, request):
        bookReportsList =  BookReport.objects.all()

        if not bookReportsList:
            return Response({"message": "No bookReport found"}, status=404)

        serializer = BookReportSerializer(bookReportsList, many=True)
        return Response({"CommunityList": serializer.data})

class LikeBookReportView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('reportNum', openapi.IN_QUERY, description="reportNum", type=openapi.TYPE_INTEGER)
    ])
    def post(self, request, *args, **kwargs):
        #data = request.query_params #swagger 테스트 용
        data = request.data
        try:
            user = User.objects.get(userNum=data['userNum'])
            bookReport = BookReport.objects.get(reportNum=data['reportNum'])
        except (User.DoesNotExist, BookReport.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_bookReport_exists = LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).exists()

        if like_bookReport_exists:
            return Response({"error": "LikeBookReport already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            like_bookReport = LikeBookReport(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport)
            like_bookReport.save()
            return Response({"message": "LikeBookReport created successfully"}, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('reportNum', openapi.IN_QUERY, description="reportNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params #swagger 테스트 용
        try:
            user = User.objects.get(userNum=data['userNum'])
            bookReport = BookReport.objects.get(reportNum=data['reportNum'])
        except (User.DoesNotExist, BookReport.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_bookReport_exists = LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).exists()

        if like_bookReport_exists:
            LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).delete()
            return Response({"message": "LikeBookReport removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeBookReport not found"}, status=status.HTTP_404_NOT_FOUND)