from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    num_likes = serializers.IntegerField()
    
    class Meta:
        model = Book
        fields = '__all__'