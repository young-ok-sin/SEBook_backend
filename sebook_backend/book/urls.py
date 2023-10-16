from django.urls import path
from . import views

urlpatterns = [
    path('bookdatas/', views.getTestDatas, name="bookdataTest"),
]