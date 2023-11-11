from django.urls import path
from .views import CreateParagraph,CommunityListRead,LikeCommunityView,UserSavedCommunity,UserWriteCommunity,SearchCommunityByAuthor,SearchCommunityByTitle,DeleteCommunity

urlpatterns = [
    path('paragraphCreate', CreateParagraph.as_view(), name='paragraphCreate'),
    path('paragraphReadAll',CommunityListRead.as_view(),name = 'CommunityListRead'),
    path('paragraphLike',LikeCommunityView.as_view(),name = 'paragraphLike'),
    path('paragraphReadLike',UserSavedCommunity.as_view(),name = 'UserSavedCommunity'),
    path('paragraphReadMy',UserWriteCommunity.as_view(),name = 'UserWriteCommunity'),
    path('searchParagraphByAuthor',SearchCommunityByAuthor.as_view(),name = 'SearchCommunityByAuthor'),
    path('searchParagraphByTitle',SearchCommunityByTitle.as_view(),name = 'SearchCommunityByTitle'),
    path('paragraphDelete',DeleteCommunity.as_view(),name = 'DeleteCommunity'),
]