from django.urls import path
from .views import GetUser

urlpatterns = [
    path('memberSearch', GetUser.as_view(), name='memberSearch'),
]