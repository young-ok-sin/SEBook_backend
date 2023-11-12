from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    num_likes = serializers.SerializerMethodField()

    def get_num_likes(self, obj):
        return obj.likebook_set.count()

    class Meta:
        model = Book
        fields = '__all__'