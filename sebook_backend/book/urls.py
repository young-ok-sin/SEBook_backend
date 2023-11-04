from django.urls import path
from .views import RecommendView,LikeBookView,SearchBookByAuthor
from .views import BookListRead,UserSavedBooks
from . import views


urlpatterns = [
    path('recommendBook/<int:userNum>', RecommendView.as_view(), name='recommend'),
    path('bookLike', LikeBookView.as_view(),name='like_book'),
    path('bookListRead', BookListRead.as_view(), name='book_list_read'),
    path('likeBookListRead',UserSavedBooks.as_view(), name='user-like-book'),
    path('searchBookByAuthor', SearchBookByAuthor.as_view(), name='book_search'),
]