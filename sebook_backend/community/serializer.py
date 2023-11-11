from rest_framework import serializers
from .models import Community,LikeCommunity,User

class CommunityReadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='isbn13_community.title')
    author = serializers.CharField(source='isbn13_community.author')
    username = serializers.CharField(source='userNum_community.name')
    like_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()
    publisher = serializers.CharField(source='isbn13_community.publisher')

    def get_like_count(self, community):
        return LikeCommunity.objects.filter(postNum_like_community=community).count()

    def get_user_liked(self, community):
        liked_users = LikeCommunity.objects.filter(postNum_like_community=community).values_list('userNum_like_community_id', flat=True)
        user_ids = User.objects.filter(userNum__in=liked_users).values_list('userNum', flat=True)
        return list(user_ids)

    class Meta:
        model = Community
        fields = ['title', 'author', 'postNum', 'contents', 'userNum_community', 'isbn13_community', 'registDate_community', 'like_count', 'user_liked', 'username', 'publisher']

class ComunitySerialzer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'