from rest_framework import serializers
from .models import BookReport,LikeBookReport,User

class BookReportReadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='isbn13_report.title')
    author = serializers.CharField(source='isbn13_report.author')
    publisher = serializers.CharField(source='isbn13_report.publisher')
    username = serializers.CharField(source='userNum_report.name')
    like_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    def get_like_count(self, book_report):
        return LikeBookReport.objects.filter(reportNum_like_bookreport=book_report).count()

    def get_user_liked(self, book_report):
        liked_users = LikeBookReport.objects.filter(reportNum_like_bookreport=book_report).values_list('userNum_like_bookreport_id', flat=True)
        user_ids = User.objects.filter(userNum__in=liked_users).values_list('userNum', flat=True)
        return list(user_ids)
    class Meta:
        model = BookReport
        fields = ['title', 'author', 'reportNum', 'reportContents', 'userNum_report', 'isbn13_report',
                'registDate_report', 'reportTitle', 'publisher', 'like_count', 'user_liked','username']

class BookReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReport
        fields = '__all__'