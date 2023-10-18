from django.shortcuts import render
from .models import LikeBook
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book
from .serializer import TestDataSerializer
from .BookRecommender import BookRecommender
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
import json

class RecommendView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recommender = BookRecommender()  # 앱이 시작할 때 한 번만 초기화합니다.
        
    def get(self, request, *args, **kwargs):
        book_title = request.GET.get('user_book')
        recommendations = self.recommender.recommend_books(book_title)
        
        # JsonResponse 객체는 Python 딕셔너리를 HTTP 응답으로 변환해줍니다.
        return JsonResponse({'recommendations': recommendations}, safe=False)
    # def get(self, request, *args, **kwargs):
    #     book_title = request.GET.get('user_book')  # 쿼리 파라미터로부터 'user_book' 값을 가져옵니다.
    #     recommendations = self.recommender.recommend_books(book_title)
    #     data = json.dumps({'recommendations': recommendations}, ensure_ascii=False)
    #     return HttpResponse(data, content_type='application/json')
    
@api_view(['GET'])
def getTestDatas(request):
    datas = Book.objects.all()
    serializer = TestDataSerializer(datas, many=True)
    return Response(serializer.data)
