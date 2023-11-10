from django.urls import path
from .views import CreateParagraph,CommunityListRead,LikeCommunity

urlpatterns = [
    path('paragraphCreate', CreateParagraph.as_view(), name='paragraphCreate'),
    path('paragraphReadAll',CommunityListRead.as_view(),name = 'CommunityListRead'),
    path('paragraphLike',LikeCommunity.as_view(),name = 'paragraphLike'),
]