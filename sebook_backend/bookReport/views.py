from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BookReport, Book, LikeBookReport
from user.models import CustomUser

from .serializer import BookReportReadSerializer,BookReportSerializer,BookReportTop5ReadSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Q
from django.db.models import Count


class CreateBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('reportContents', openapi.IN_QUERY, description="reportContents", type=openapi.TYPE_STRING),
        openapi.Parameter('reportTitle', openapi.IN_QUERY, description="reportTitle", type=openapi.TYPE_STRING),
        openapi.Parameter('isbn13_report', openapi.IN_QUERY, description="isbn13_report", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        #테스트 용
        # reportContents = request.GET.get('reportContents')
        # reportTitle = request.GET.get('reportTitle')
        # isbn13_report = request.GET.get('isbn13_report')
        reportContents = request.data.get('reportContents')
        reportTitle = request.data.get('reportTitle')
        isbn13_report = request.data.get('isbn13_report')
        
        try:
            user = request.user
        except CustomUser.DoesNotExist:
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
        
        serializer = BookReportSerializer(book_report)
        return JsonResponse(serializer.data)
    
class UpdateBookReport(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('reportNum', openapi.IN_QUERY, description="Report number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('reportContents', openapi.IN_QUERY, description="Report contents", type=openapi.TYPE_STRING),
        openapi.Parameter('reportTitle', openapi.IN_QUERY, description="Report title", type=openapi.TYPE_STRING)
    ])
    def put(self, request):
        #swagger테스트 용
        # reportNum = request.GET.get('reportNum')
        # reportContents = request.GET.get('reportContents')
        # reportTitle = request.GET.get('reportTitle')
        
        #프론트 용
        reportNum = request.data.get('reportNum')
        reportContents = request.data.get('reportContents')
        reportTitle = request.data.get('reportTitle')

        try:
            book_report = BookReport.objects.get(reportNum=reportNum)
        except BookReport.DoesNotExist:
            return Response({"error": "Book report does not exist"}, status=404)

        book_report.reportContents = reportContents
        book_report.reportTitle = reportTitle
        book_report.save()

        serializer = BookReportReadSerializer(book_report)
        return Response(serializer.data)

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
    def get(self, request):
        try:
            user = request.user
            like_bookreports = LikeBookReport.objects.filter(userNum_like_bookreport=user)
            saved_books = [like_bookreport.reportNum_like_bookreport for like_bookreport in like_bookreports]
            serializer = BookReportReadSerializer(saved_books, many=True)
            return Response({"likeBookReportList": serializer.data})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UserWriteBookReports(APIView):
    def get(self, request):
        try:
            user = request.user
            bookreports = BookReport.objects.filter(userNum_report=user)
            serializer = BookReportReadSerializer(bookreports, many=True)
            return Response({"userBookReportList": serializer.data})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class ReadAllBookReport(APIView):
    def get(self, request):
        response_data = {}
        
        if request.user.is_authenticated:
            reportNum = request.user
        
        # 사용자가 작성한 독후감들을 가져옴
            user_reports = BookReport.objects.filter(userNum_report=reportNum)
        
        # 사용자가 공감한 독후감들을 가져옴
            liked_reports = BookReport.objects.filter(likebookreport__userNum_like_bookreport=reportNum)
        
            userLikeReports = liked_reports.values_list('reportNum', flat=True)
            userWriteReports = user_reports.values_list('reportNum', flat=True)

            response_data["userLikeReports"] = list(userLikeReports)
            response_data["userWriteReports"] = list(userWriteReports)
        
        all_reports = BookReport.objects.all()
        all_reports_serializer = BookReportReadSerializer(all_reports, many=True)
        
        response_data["allReports"] =all_reports_serializer.data
        return Response(response_data)

class LikeBookReportView(APIView):
    def post(self, request, *args, **kwargs):
        #swagger 테스트 용
        #data = request.query_params
        
        #프론트 용 
        data = request.data
        try:
            user = request.user
            bookReport = BookReport.objects.get(reportNum=data['reportNum'])
        except (CustomUser.DoesNotExist, BookReport.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_bookReport_exists = LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).exists()

        if like_bookReport_exists:
            return Response({"error": "LikeBookReport already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            like_bookReport = LikeBookReport(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport)
            like_bookReport.save()
            return Response({"message": "LikeBookReport created successfully"}, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('reportNum', openapi.IN_QUERY, description="reportNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params #swagger 테스트 용
        try:
            user = request.user
            bookReport = BookReport.objects.get(reportNum=data['reportNum'])
        except (CustomUser.DoesNotExist, BookReport.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_bookReport_exists = LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).exists()

        if like_bookReport_exists:
            LikeBookReport.objects.filter(userNum_like_bookreport=user, reportNum_like_bookreport=bookReport).delete()
            return Response({"message": "LikeBookReport removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeBookReport not found"}, status=status.HTTP_404_NOT_FOUND)

class SearchBookReportByTitle(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Search by title", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        title = request.query_params.get('title', None)
        if title is None:
            return Response({"error": "title parameter is required"}, status=400)

        bookreports = BookReport.objects.filter(reportTitle__icontains=title)
        if not bookreports.exists():
            return Response({"message": f"No results found for title: {title}"}, status=404)

        serializer = BookReportReadSerializer(bookreports, many=True)
        return Response(serializer.data, status=200)

class TopRatedBookReports(APIView):
    def get(self, request):
        top_reports = BookReport.objects.annotate(like_count=Count('likebookreport')).order_by('-like_count', 'registDate_report')[:5]
        serializer = BookReportTop5ReadSerializer(top_reports, many=True)
        return Response(serializer.data, status=200)