from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Community,User,Book,LikeCommunity
from .serializer import ComunitySerialzer,CommunityReadSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Q

class CreateParagraph(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('contents', openapi.IN_QUERY, description="Paragraph", type=openapi.TYPE_STRING),
        openapi.Parameter('userNum_community', openapi.IN_QUERY, description="userNum_community", type=openapi.TYPE_INTEGER),
        openapi.Parameter('isbn13_community', openapi.IN_QUERY, description="isbn13_community", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        #테스트 용
        # contents = request.GET.get('contents')
        # userNum_community = request.GET.get('userNum_community')
        # isbn13_community = request.GET.get('isbn13_community')
        contents = request.data.get('contents')
        userNum_community = request.data.get('userNum_community')
        isbn13_community = request.data.get('isbn13_community')
        try:
            user = User.objects.get(userNum=userNum_community)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)
        try:
            book = Book.objects.get(isbn13=isbn13_community)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist."}, status=404)
        
        community = Community.objects.create(
            contents=contents,
            userNum_community=user,
            isbn13_community=book
        )
        
        serializer = ComunitySerialzer(community)
        return JsonResponse(serializer.data)

class CommunityListRead(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum')

        # 사용자가 작성한 커뮤니티 글들을 가져옴
        user_community = Community.objects.filter(userNum_community=userNum)
        user_community_serializer = CommunityReadSerializer(user_community, many=True)

        # 사용자가 좋아요한 커뮤니티 글들을 가져옴
        liked_community = Community.objects.filter(likecommunity__userNum_like_community=userNum)
        liked_community_serializer = CommunityReadSerializer(liked_community, many=True)

        userLikedPosts = liked_community.values_list('postNum', flat=True)
        userWrittenPosts = user_community.values_list('postNum', flat=True)

        all_community = Community.objects.all()
        all_community_serializer = CommunityReadSerializer(all_community, many=True)

        response_data = {
            "userLikedPosts": list(userLikedPosts),
            "userWrittenPosts": list(userWrittenPosts),
            "allPosts": all_community_serializer.data
        }
        return Response(response_data)

class LikeCommunityView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('postNum', openapi.IN_QUERY, description="postNum", type=openapi.TYPE_INTEGER)
    ])
    def post(self, request, *args, **kwargs):
        #data = request.query_params #swagger 테스트 용
        data = request.data
        try:
            user = User.objects.get(userNum=data['userNum'])
            community = Community.objects.get(postNum=data['postNum'])
        except (User.DoesNotExist, Community.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_community_exists = LikeCommunity.objects.filter(userNum_like_community=user, postNum_like_community=community).exists()

        if like_community_exists:
            return Response({"error": "LikeCommunity already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            like_community = LikeCommunity(userNum_like_community=user, postNum_like_community=community)
            like_community.save()
            return Response({"message": "LikeBook created successfully"}, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('postNum', openapi.IN_QUERY, description="postNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params #swagger 테스트 용
        try:
            user = User.objects.get(userNum=data['userNum'])
            community = Community.objects.get(postNum=data['postNum'])
        except (User.DoesNotExist, Community.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_community_exists = LikeCommunity.objects.filter(userNum_like_community=user, postNum_like_community=community).exists()

        if like_community_exists:
            LikeCommunity.objects.filter(userNum_like_community=user, postNum_like_community=community).delete()
            return Response({"message": "LikeCommunity removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeCommunity not found"}, status=status.HTTP_404_NOT_FOUND)

class UserSavedCommunity(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum')

        try:
            user = User.objects.get(userNum=userNum)
            saved_communities = LikeCommunity.objects.filter(userNum_like_community=user)
            saved_posts = [like_community.postNum_like_community for like_community in saved_communities]
            serializer = CommunityReadSerializer(saved_posts, many=True)
            return Response({"savedCommunityList": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UserWriteCommunity(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('userNum', openapi.IN_QUERY, description="User number", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        userNum = request.query_params.get('userNum')

        try:
            user = User.objects.get(userNum=userNum)
            user_community = Community.objects.filter(userNum_community=user)
            serializer = CommunityReadSerializer(user_community, many=True)
            return Response({"userCommunityList": serializer.data})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class SearchCommunityByAuthor(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('author', openapi.IN_QUERY, description="Search by author", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        author = request.query_params.get('author', None)
        if author is None:
            return Response({"error": "Author parameter is required"}, status=400)

        communities = Community.objects.filter(Q(isbn13_community__author__icontains=author))
        if not communities.exists():
            return Response({"message": f"No results found for author: {author}"}, status=404)

        serializer = CommunityReadSerializer(communities, many=True)
        return Response(serializer.data, status=200)

class SearchCommunityByTitle(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="search by title", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        title = request.query_params.get('title', None)
        if title is None:
            return Response({"error": "title parameter is required"}, status=400)

        communities = Community.objects.filter(Q(isbn13_community__title__icontains=title))
        if not communities.exists():
            return Response({"message": f"No results found for author: {title}"}, status=404)

        serializer = CommunityReadSerializer(communities, many=True)
        return Response(serializer.data, status=200)

class DeleteCommunity(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('postNum', openapi.IN_QUERY, description="postNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request):
        community_num = request.query_params
        try:
            community = Community.objects.get(postNum=community_num['postNum'])
        except Community.DoesNotExist:
            return Response({"error": "community not found"}, status=status.HTTP_404_NOT_FOUND)
        community.delete()
        return Response({"message": "community deleted"}, status=status.HTTP_204_NO_CONTENT)
    