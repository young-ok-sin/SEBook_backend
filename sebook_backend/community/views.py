from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Community, Book, LikeCommunity
from user.models import CustomUser
from django.core.paginator import Paginator
from .serializer import ComunitySerialzer,CommunityReadSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Q

class CreateParagraph(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('contents', openapi.IN_QUERY, description="Paragraph", type=openapi.TYPE_STRING),
        openapi.Parameter('isbn13_community', openapi.IN_QUERY, description="isbn13_community", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        #테스트 용
        # contents = request.GET.get('contents')
        # isbn13_community = request.GET.get('isbn13_community')
        contents = request.data.get('contents')
        isbn13_community = request.data.get('isbn13_community')
        try:
            user = request.user
        except CustomUser.DoesNotExist:
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
        openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):

        all_community = Community.objects.all().order_by('-registDate_community')
        paginator = Paginator(all_community, 4)

        page_number = request.query_params.get('page')
        page_obj = paginator.get_page(page_number)
        
        all_community_serializer = CommunityReadSerializer(page_obj, many=True)

        return Response({
            'total_pages': paginator.num_pages, 
            'results': all_community_serializer.data
        })

class LikeCommunityView(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('postNum', openapi.IN_QUERY, description="postNum", type=openapi.TYPE_INTEGER)
    ])
    def post(self, request, *args, **kwargs):
        #data = request.query_params
        data = request.data
        try:
            user = request.user
            community = Community.objects.get(postNum=data['postNum'])
        except (CustomUser.DoesNotExist, Community.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_community = LikeCommunity.objects.filter(userNum_like_community=user, postNum_like_community=community).first()

        if like_community:
            like_community.delete()
            return Response({"message": "LikeCommunity removed successfully"}, status=status.HTTP_200_OK)
        else:
            LikeCommunity.objects.create(userNum_like_community=user, postNum_like_community=community)
            return Response({"message": "LikeCommunity created successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('postNum', openapi.IN_QUERY, description="postNum", type=openapi.TYPE_INTEGER)
    ])
    def delete(self, request, *args, **kwargs):
        data = request.query_params
        try:
            user = request.user
            community = Community.objects.get(postNum=data['postNum'])
        except (CustomUser.DoesNotExist, Community.DoesNotExist):
            return Response({"error": "User or post not found"}, status=status.HTTP_404_NOT_FOUND)

        like_community = LikeCommunity.objects.filter(userNum_like_community=user, postNum_like_community=community).first()

        if like_community:
            like_community.delete()
            return Response({"message": "LikeCommunity removed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "LikeCommunity not found"}, status=status.HTTP_404_NOT_FOUND)

class UserSavedCommunity(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        try:
            user = request.user
            saved_communities = LikeCommunity.objects.filter(userNum_like_community=user)
            saved_posts = [like_community.postNum_like_community for like_community in saved_communities]
            
            paginator = Paginator(saved_posts, 4)

            page_number = request.query_params.get('page')
            
            page_obj = paginator.get_page(page_number)
            
            all_community_serializer = CommunityReadSerializer(page_obj, many=True)

            return Response({
                'total_pages': paginator.num_pages, 
                'results': all_community_serializer.data
            })
            # serializer = CommunityReadSerializer(saved_posts, many=True)
            # return Response({"savedCommunityList": serializer.data})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UserWriteCommunity(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        try:
            user = request.user
            user_community = Community.objects.filter(userNum_community=user).order_by('-registDate_community')
            
            paginator = Paginator(user_community, 4)

            page_number = request.query_params.get('page')
            page_obj = paginator.get_page(page_number)
            
            all_community_serializer = CommunityReadSerializer(page_obj, many=True)

            return Response({
                'total_pages': paginator.num_pages, 
                'results': all_community_serializer.data
            })
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class SearchCommunityByAuthor(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('author', openapi.IN_QUERY, description="Search by author", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        author = request.query_params.get('author', None)
        if author is None:
            return Response({"error": "Author parameter is required"}, status=400)

        # Community 모델에서 작가(author)를 포함하는 커뮤니티 게시물을 검색
        communities = Community.objects.filter(isbn13_community__author__icontains=author).order_by('-registDate_community')

        # 페이징 처리
        paginator = Paginator(communities, 4)
        page_number = request.query_params.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = CommunityReadSerializer(page_obj, many=True)

        return Response({
            'total_pages': paginator.num_pages, 
            'results': serializer.data
        }, status=200)

class SearchCommunityByTitle(APIView):
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="search by title", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="page", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        title = request.query_params.get('title', None)
        if title is None:
            return Response({"error": "title parameter is required"}, status=400)

        communities = Community.objects.filter(isbn13_community__title__icontains=title).order_by('-registDate_community')
        if not communities.exists():
            return Response({"message": f"No results found for title: {title}"}, status=404)

        # 페이징 처리
        paginator = Paginator(communities, 4)
        page_number = request.query_params.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = CommunityReadSerializer(page_obj, many=True)
        return Response({
            'total_pages': paginator.num_pages, 
            'results': serializer.data
        }, status=200)

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
    