from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, LikeBook
from user.models import CustomUser

from .serializer import BookSerializer
from .BookRecommender import BookRecommender
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import connection
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.contrib.auth.models import AnonymousUser

class RecommendView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommender = BookRecommender()

    def get(self, request, *args, **kwargs): 
        userNum = request.user
        if isinstance(userNum, AnonymousUser):  # 로그인하지 않은 경우
            recommendations = self.recommender.recommend_randomBooks()  # userNum 인자 생략
            recommendations = {'recommendations': recommendations, 'message': "도서 추천을 받아보고 싶으시다면 로그인을 해주세요"}
            return JsonResponse(recommendations, status=200)

        like_books = LikeBook.objects.filter(userNum_like_book=userNum)
        if not like_books:
            recommendations = self.recommender.recommend_randomBooks()  # userNum 인자 생략
            recommendations = {'recommendations': recommendations, 'message': "저장한 도서가 없습니다. 랜덤 도서를 추천합니다."}
            return JsonResponse(recommendations, status=200)

        try:
            recommendations = self.recommender.recommend_books(userNum)  # userNum 인자 전달
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        if not recommendations:
            return JsonResponse({"message": "No recommendations found for this user"}, status=404)

        return JsonResponse({'recommendations': recommendations}, safe=False)

# class RecommendView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.recommender = BookRecommender()

#     def get(self, request, *args, **kwargs): 
#         userNum = request.user
#         if not userNum:
#             recommendations = self.recommender.recommend_books()
#             recommendations['message'] = "도서 추천을 받아보고 싶으시다면 로그인을 해주세요"
#             return JsonResponse(recommendations, status=200)
#         try:
#             recommendations = self.recommender.recommend_books(userNum)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#         if not recommendations:
#             return JsonResponse({"message": "No recommendations found for this user"}, status=404)

#         return JsonResponse({'recommendations': recommendations}, safe=False)

class BookListRead(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else AnonymousUser()
        book_list = Book.objects.all()

        if not book_list:
            return Response({"message": "No books found"}, status=404)

        serializer = BookSerializer(book_list, many=True)

        # 사용자가 좋아한 도서의 목록을 가져옴
        if isinstance(user, AnonymousUser):
            liked_books_list = []
        else:
            liked_books = LikeBook.objects.filter(userNum_like_book=user).values_list('isbn13_like_book', flat=True)
            liked_books_list = list(liked_books)

        return Response({"bookList": serializer.data, "likedBooks": liked_books_list})

class LikeBookView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
    ])
    def post(self, request, *args, **kwargs):
        #data = request.query_params # for swagger test
        data = request.data
        try:
            user = request.user
            book = Book.objects.get(isbn13=data['isbn13'])
        except (CustomUser.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

        created = LikeBook.objects.get_or_create(userNum_like_book=user, isbn13_like_book=book)

        if not created:
            return Response({"error": "LikeBook already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        book.num_likes += 1  # num_likes 필드 업데이트
        book.save()
        return Response({"message": "LikeBook created successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params
        try:
            user = request.user
            book = Book.objects.get(isbn13=data['isbn13'])
        except (CustomUser.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

        like_book = LikeBook.objects.filter(userNum_like_book=user, isbn13_like_book=book).first()

        if like_book:
            like_book.delete()
            book.num_likes -= 1  # num_likes 필드 업데이트
            book.save()
            return Response({"message": "LikeBook removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeBook not found"}, status=status.HTTP_404_NOT_FOUND)

class UserSavedBooks(APIView):
    def get(self, request):
        user = request.user
        like_books = LikeBook.objects.filter(userNum_like_book=user)
        
        saved_books = [like_book.isbn13_like_book for like_book in like_books]
        
        serializer = BookSerializer(saved_books, many=True)
        
        return Response({"likeBookList": serializer.data})

class SearchBookByAuthor(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('author', openapi.IN_QUERY, description="search by author", type=openapi.TYPE_STRING)
    ])
    def get(self, request, *args, **kwargs):
        author = request.query_params.get('author', None)
        if author is None:
            return Response({"error": "Author parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(Q(author__icontains=author))
        if not books.exists():
            return Response({"message": author+"에 대한 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchBookByTitle(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="search by title", type=openapi.TYPE_STRING)
    ])
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)
        if title is None:
            return Response({"error": "title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        books = Book.objects.filter(Q(title__icontains=title))
        if not books.exists():
            return Response({"message": title+"에 대한 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopLikedBooks(APIView):
    def get(self, request):
        top_liked_books = Book.objects.order_by('-num_likes', 'isbn13')[:5]
        serializer = BookSerializer(top_liked_books, many=True)
        return Response({"bestsellerList":serializer.data})
