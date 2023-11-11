from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BookReport,User,Book,LikeBookReport
from .serializer import BookReportReadSerializer,BookReportSerializer
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
        #테스트 용
        # userNum_report = request.GET.get('userNum_report')
        # reportContents = request.GET.get('reportContents')
        # reportTitle = request.GET.get('reportTitle')
        # isbn13_report = request.GET.get('isbn13_report')
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
            return Response({"userBookReportList": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class ReadAllBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        reportNum = request.query_params.get('userNum')
        
        # 사용자가 작성한 독후감들을 가져옴
        user_reports = BookReport.objects.filter(userNum_report=reportNum)
        user_reports_serializer = BookReportReadSerializer(user_reports, many=True)
        
        # 사용자가 공감한 독후감들을 가져옴
        liked_reports = BookReport.objects.filter(likebookreport__userNum_like_bookreport=reportNum)
        liked_reports_serializer = BookReportReadSerializer(liked_reports, many=True)
        
        userLikeReports = liked_reports.values_list('reportNum', flat=True)
        userWriteReports = user_reports.values_list('reportNum', flat=True)
        
        all_reports = BookReport.objects.all()
        all_reports_serializer = BookReportReadSerializer(all_reports, many=True)
        
        response_data = {
            "userLikeReports": list(userLikeReports),
            "userWriteReports": list(userWriteReports),
            "allReports": all_reports_serializer.data
        }
        return Response(response_data)

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