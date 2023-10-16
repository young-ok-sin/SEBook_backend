from django.db import models
from user.models import User
from book.models import Book

# Create your models here.


class Community(models.Model):
    postNum = models.AutoField(primary_key=True)
    contents = models.TimeField(null = False)
    userNum_community = models.ForeignKey(User,on_delete=models.CASCADE)
    isbn13_community = models.ForeignKey(Book,on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'commmunity'

class LikeCommunity(models.Model):
    like_communityNum = models.AutoField(primary_key=True)
    userNum_like_community = models.ForeignKey(User,on_delete=models.CASCADE)
    postNum_like_community = models.ForeignKey(Community,on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'like_community'