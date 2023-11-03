from django.urls import path
from .views import RecommendView,like_book
from .views import BookListRead,UserSavedBooks
from . import views

urlpatterns = [
    path('recommendBook', RecommendView.as_view(), name='recommend'),
    path('bookLike', like_book),
    path('bookListRead', BookListRead.as_view(), name='book-list-read'),
    path('likeBookListRead', UserSavedBooks.as_view(), name='user-like-book'),
]
    # path('recommendBook/<int:userNum>', RecommendView.as_view(), name='recommend'),