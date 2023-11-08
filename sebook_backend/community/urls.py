from django.urls import path
from .views import CreateParagraph

urlpatterns = [
    path('paragraphCreate', CreateParagraph.as_view(), name='paragraphCreate'),
]