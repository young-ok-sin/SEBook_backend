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

class RecommendView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommender = BookRecommender()  # 앱이 시작할 때 한 번만 초기화합니다.
    # def get(self, request, *args, **kwargs):
    #     userNum = kwargs.get('userNum')
    #     recommendations = self.recommender.recommend_books(userNum)

    #     return HttpResponse(json.dumps({'recommendations': recommendations}, ensure_ascii=False), content_type='application/json; charset=utf8')
    def get(self, request, *args, **kwargs):
        userNum = request.GET.get('userNum')
        recommendations = self.recommender.recommend_books(userNum)

        return JsonResponse({'recommendations': recommendations}, safe=False)        


class BookListRead(APIView):
    def get(self, request):
        # 도서 목록 조회
        book_list = Book.objects.all()   
        # 시리얼라이즈
        serializer = BookSerializer(book_list, many=True)
        
        # JSON 응답 반환
        return Response({"bookList": serializer.data})


@csrf_exempt
def like_book_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # 클라이언트로부터 받은 데이터를 로드합니다.
        user = User.objects.get(userNum=data['userNum'])  # 사용자 정보를 가져옵니다.
        book = Book.objects.get(isbn13=data['isbn13'])  # 도서 정보를 가져옵니다.
        like_book = LikeBook(userNum_like_book=user, isbn13_like_book=book)  # LikeBook 객체를 생성합니다.
        like_book.save()  # 데이터베이스에 저장합니다.
        return JsonResponse({"message": "LikeBook created successfully"}, status=201)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


class UserSavedBooks(APIView):
    def get(self, request):
        userNum = request.query_params.get('userNum')
        # 사용자가 저장한 도서 조회
        user = User.objects.get(userNum=userNum)
        like_books = LikeBook.objects.filter(userNum_like_book=user)
        
        # 도서 목록 추출
        saved_books = [like_book.isbn13_like_book for like_book in like_books]
        
        # 시리얼라이즈
        serializer = BookSerializer(saved_books, many=True)
        
        # JSON 응답 반환
        return Response({"likeBookList": serializer.data})
