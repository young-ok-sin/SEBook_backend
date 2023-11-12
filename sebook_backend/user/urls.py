from django.urls import path
from .views import GetUser,UserSignUp,LoginView

urlpatterns = [
    path('memberSearch', GetUser.as_view(), name='memberSearch'),
    path('memberReg', UserSignUp.as_view(), name='memberReg'),
    path('login', LoginView.as_view(), name='memberReg'),
]