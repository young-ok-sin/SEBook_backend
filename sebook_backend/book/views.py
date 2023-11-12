from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, LikeBook, User
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
from django.db.models import Count

class RecommendView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommender = BookRecommender()

    def get(self, request, *args, **kwargs): 
        userNum = kwargs.get('userNum')
        if not userNum:
            recommendations = self.recommender.recommend_books()
            recommendations['message'] = "도서 추천을 받아보고 싶으시다면 로그인을 해주세요"
            return JsonResponse(recommendations, status=200)
#     def get(self, request, *args, **kwargs): # params 사용 시
#         userNum = request.GET.get('userNum')
#         recommendations = self.recommender.recommend_books(userNum)
        try:
            recommendations = self.recommender.recommend_books(userNum)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        if not recommendations:
            return JsonResponse({"message": "No recommendations found for this user"}, status=404)

        return JsonResponse({'recommendations': recommendations}, safe=False)

class BookListRead(APIView):
    def get(self, request):
        book_list = Book.objects.all()#[:5] #swagger test 시 사용

        if not book_list:
            return Response({"message": "No books found"}, status=404)

        serializer = BookSerializer(book_list, many=True)
        return Response({"bookList": serializer.data})

# class RecommendView(APIView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.recommender = BookRecommender()  # 앱이 시작할 때 한 번만 초기화
#     # def get(self, request, *args, **kwargs):
#     #     userNum = kwargs.get('userNum')
#     #     recommendations = self.recommender.recommend_books(userNum)

#     #     return HttpResponse(json.dumps({'recommendations': recommendations}, ensure_ascii=False), content_type='application/json; charset=utf8') # 쿼리스트링 사용 시
#     def get(self, request, *args, **kwargs): # params 사용 시
#         userNum = request.GET.get('userNum')
#         recommendations = self.recommender.recommend_books(userNum)

#         return JsonResponse({'recommendations': recommendations}, safe=False)

class LikeBookView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
    ])
    def post(self, request, *args, **kwargs):
        #data = request.query_params #swagger 테스트 용
        data = request.data
        try:
            user = User.objects.get(userNum=data['userNum'])
            book = Book.objects.get(isbn13=data['isbn13'])
        except (User.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

        like_book, created = LikeBook.objects.get_or_create(userNum_like_book=user, isbn13_like_book=book)

        if not created:
            return Response({"error": "LikeBook already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        book.num_likes += 1  # num_likes 필드 업데이트
        book.save()

        return Response({"message": "LikeBook created successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params
        try:
            user = User.objects.get(userNum=data['userNum'])
            book = Book.objects.get(isbn13=data['isbn13'])
        except (User.DoesNotExist, Book.DoesNotExist):
            return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

        like_book = LikeBook.objects.filter(userNum_like_book=user, isbn13_like_book=book).first()

        if like_book:
            like_book.delete()
            book.num_likes -= 1  # num_likes 필드 업데이트
            book.save()
            return Response({"message": "LikeBook removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeBook not found"}, status=status.HTTP_404_NOT_FOUND)

# class LikeBookView(APIView):
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
#         openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
#     ])
#     def post(self, request, *args, **kwargs):
#         # data = request.query_params #swagger 테스트 용
#         data = request.data
#         try:
#             user = User.objects.get(userNum=data['userNum'])
#             book = Book.objects.get(isbn13=data['isbn13'])
#         except (User.DoesNotExist, Book.DoesNotExist):
#             return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

#         like_book_exists = LikeBook.objects.filter(userNum_like_book=user, isbn13_like_book=book).exists()

#         if like_book_exists:
#             return Response({"error": "LikeBook already exists"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             like_book = LikeBook(userNum_like_book=user, isbn13_like_book=book)
#             like_book.save()
#             return Response({"message": "LikeBook created successfully"}, status=status.HTTP_201_CREATED)
    
#     @swagger_auto_schema(manual_parameters=[
#         openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
#         openapi.Parameter('isbn13', openapi.IN_QUERY, description="Book ISBN", type=openapi.TYPE_STRING)
#     ])
#     def delete(self, request, *args, **kwargs):
#         data = request.query_params #swagger 테스트 용
#         try:
#             user = User.objects.get(userNum=data['userNum'])
#             book = Book.objects.get(isbn13=data['isbn13'])
#         except (User.DoesNotExist, Book.DoesNotExist):
#             return Response({"error": "User or Book not found"}, status=status.HTTP_404_NOT_FOUND)

#         like_book_exists = LikeBook.objects.filter(userNum_like_book=user, isbn13_like_book=book).exists()

#         if like_book_exists:
#             LikeBook.objects.filter(userNum_like_book=user, isbn13_like_book=book).delete()
#             return Response({"message": "LikeBook removed successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "LikeBook not found"}, status=status.HTTP_404_NOT_FOUND)
        
class UserSavedBooks(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):

        userNum = request.query_params.get('userNum')
        
        user = User.objects.get(userNum=userNum)
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
        
        # 'icontains'를 사용하여 검색어를 포함하는 도서만 필터링합니다.
        books = Book.objects.filter(Q(title__icontains=title))
        if not books.exists():
            return Response({"message": title+"에 대한 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        # 검색 결과를 직렬화합니다.
        
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TopLikedBooks(APIView):
    def get(self, request):
        top_liked_books = Book.objects.annotate(num_likes=Count('likebook')).order_by('-num_likes', 'isbn13')[:5] #좋아요 내림차순, isbn13 오름차순 정렬
        serializer = BookSerializer(top_liked_books, many=True)
        return Response(serializer.data)
