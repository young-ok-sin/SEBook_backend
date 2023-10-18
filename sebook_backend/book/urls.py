from django.urls import path
from .views import RecommendView
from . import views

# urlpatterns = [
#     path('bookdatas/', views.getTestDatas, name="bookdataTest"),
#     path('recommendBook/<str:book_title>', RecommendView.as_view(), name='recommend'),
# ]

urlpatterns = [
    path('bookdatas/', views.getTestDatas, name="bookdataTest"),
    path('recommendBook', RecommendView.as_view(), name='recommend'),  # '<str:book_title>' 부분 제거
]