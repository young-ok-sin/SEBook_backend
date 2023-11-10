from django.db import models
from user.models import User
from book.models import Book

# Create your models here.

class Community(models.Model):
    postNum = models.AutoField(primary_key=True)
    contents = models.TextField(null = False)
    userNum_community = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userNum_community')
    isbn13_community = models.ForeignKey(Book,on_delete=models.CASCADE,db_column='isbn13_community')
    
    class Meta:
        managed = False
        db_table = 'community'

class LikeCommunity(models.Model):
    like_communityNum = models.AutoField(primary_key=True)
    userNum_like_community = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userNum_like_community')
    postNum_like_community = models.ForeignKey(Community,on_delete=models.CASCADE,db_column='postNum_like_community')
    
    class Meta:
        managed = False
        db_table = 'like_community'