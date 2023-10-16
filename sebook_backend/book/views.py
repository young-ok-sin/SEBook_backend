from django.shortcuts import render
from .models import LikeBook
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializer import TestDataSerializer
from . import BookRecommender

@api_view(['GET'])
def getTestDatas(request):
    datas = Book.objects.all()
    serializer = TestDataSerializer(datas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recommend_books(request):
    # Initialize the book recommender.
    recommender = BookRecommender()

    # Collect user's books data from your database.
    user_books = LikeBook.objects.filter(userNum_like_book=request.user.id)
    
    if not user_books.exists():
        return JsonResponse([], safe=False)

    # Get the title and depth3 of the first liked book of the user.
    first_liked_book = user_books.first().isbn13_like_book
    user_book_title = first_liked_book.title
    user_book_depth3 = first_liked_book.depth3

    # Apply your recommendation algorithm and get the result.
    recommended_titles = recommender.recommend_books(user_book_title, user_book_depth3)

    # Convert recommended titles to list of dictionaries with title and depth3 for JSON response.
    recommended_books_data = [{'title': title, 'depth3': depth} for title, depth in recommended_titles]

    return JsonResponse(recommended_books_data, safe=False)