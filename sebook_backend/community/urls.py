from django.urls import path
from .views import CreateParagraph,CommunityListRead,LikeCommunityView,UserSavedCommunity,UserWriteCommunity

urlpatterns = [
    path('paragraphCreate', CreateParagraph.as_view(), name='paragraphCreate'),
    path('paragraphReadAll',CommunityListRead.as_view(),name = 'CommunityListRead'),
    path('paragraphLike',LikeCommunityView.as_view(),name = 'paragraphLike'),
    path('paragraphReadLike',UserSavedCommunity.as_view(),name = 'UserSavedCommunity'),
    path('paragraphReadMy',UserWriteCommunity.as_view(),name = 'UserWriteCommunity'),
]