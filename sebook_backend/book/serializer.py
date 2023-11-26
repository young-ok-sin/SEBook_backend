from rest_framework import serializers
from .models import Book, LikeBook, CustomUser

class BookSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    def get_like_count(self, book):
        return LikeBook.objects.filter(isbn13_like_book=book).count()

    def get_user_liked(self, book):
        liked_users = LikeBook.objects.filter(isbn13_like_book=book).values_list('userNum_like_book_id', flat=True)
        user_ids = CustomUser.objects.filter(userNum__in=liked_users).values_list('userNum', flat=True)
        return list(user_ids)

    class Meta:
        model = Book
        fields = '__all__'