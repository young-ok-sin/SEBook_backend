from django.urls import path
from .views import GetUser,UserSignUp

urlpatterns = [
    path('memberSearch', GetUser.as_view(), name='memberSearch'),
    path('memberReg', UserSignUp.as_view(), name='memberReg'),
]