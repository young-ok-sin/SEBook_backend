from rest_framework import serializers
from .models import Community

class CommunitySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='isbn13_community.title')
    author = serializers.CharField(source='isbn13_community.author')
    
    class Meta:
        model = Community
        fields = ['title', 'author', 'postNum', 'contents', 'userNum_community', 'isbn13_community']

class ComunityCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'