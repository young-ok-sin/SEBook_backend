from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, LikeBook
from user.models import CustomUser
from .serializer import BookSerializer,ReadBookAllSerializer
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
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count

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
            return JsonResponse({"message": "이 사용자에 대한 추천이 없습니다."}, status=404)

        # 최근에 저장한 도서와 같은 카테고리인 도서들을 먼저 새로운 리스트에 담기
        latest_book_category = like_books.latest('like_bookNum').isbn13_like_book.categoryId_book_id
        category_books = [book for book in recommendations if book['categoryId'] == latest_book_category]

        # 나머지 도서들을 리스트에 담기
        remaining_books = [book for book in recommendations if book['categoryId'] != latest_book_category]

        # 최근에 저장한 도서와 같은 카테고리인 도서들을 먼저 추가한 후, 나머지 도서들을 추가
        final_recommendations = category_books + remaining_books

        # final_recommendations = final_recommendations[::-1]
        return JsonResponse({'recommendations': final_recommendations}, safe=False)

# class RecommendView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.recommender = BookRecommender()

#     def get(self, request, *args, **kwargs): 
#         userNum = request.user
#         if isinstance(userNum, AnonymousUser):  # 로그인하지 않은 경우
#             recommendations = self.recommender.recommend_randomBooks()  # userNum 인자 생략
#             recommendations = {'recommendations': recommendations, 'message': "도서 추천을 받아보고 싶으시다면 로그인을 해주세요"}
#             return JsonResponse(recommendations, status=200)

#         like_books = LikeBook.objects.filter(userNum_like_book=userNum)
#         if not like_books:
#             recommendations = self.recommender.recommend_randomBooks()  # userNum 인자 생략
#             recommendations = {'recommendations': recommendations, 'message': "저장한 도서가 없습니다. 랜덤 도서를 추천합니다."}
#             return JsonResponse(recommendations, status=200)

#         try:
#             recommendations = self.recommender.recommend_books(userNum)  # userNum 인자 전달
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#         if not recommendations:
#             return JsonResponse({"message": "No recommendations found for this user"}, status=404)
        
#         recommendations = recommendations[::-1]
#         return JsonResponse({'recommendations': recommendations}, safe=False)

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
        book_list = Book.objects.all()#[:5]
        if not book_list:
            return Response({"message": "No books found"}, status=404)

        serializer = ReadBookAllSerializer(book_list, many=True)

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
        #data = request.query_params
        data = request.data
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
            LikeBook.objects.create(userNum_like_book=user, isbn13_like_book=book)
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

        return Response({"bookList": serializer.data}, status=status.HTTP_200_OK)


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

        return Response({"bookList": serializer.data}, status=status.HTTP_200_OK)

class TopLikedBooks(APIView):
    def get(self, request):
        top_liked_books = Book.objects.order_by('-num_likes', 'isbn13')[:5]
        serializer = BookSerializer(top_liked_books, many=True)
        return Response({"bestsellerList": serializer.data})

# class TopLikedBooks(APIView):
#     def get(self, request):
#         top_liked_books = Book.objects.annotate(total_likes=Count('likebook')).order_by('-total_likes', 'isbn13')[:5]
#         serializer = BookSerializer(top_liked_books, many=True)
#         return Response({"bestsellerList": serializer.data})
