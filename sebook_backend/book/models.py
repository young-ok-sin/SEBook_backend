from django.db import models
from user.models import User
# Create your models here.

class Book(models.Model):
    isbn13 = models.CharField(max_length=13,primary_key=True,null = False)
    title = models.CharField(max_length=200,null = False)
    author = models.TextField(null = False)
    cover = models.TextField(null = False)
    categoryId = models.IntegerField(null = False)
    description = models.TextField()
    publisher = models.CharField(max_length=30,null = False)
    mallType = models.CharField(max_length=10,null = False)
    priceStandard = models.IntegerField(null = False)
    link = models.TextField(null = False)
    adult = models.CharField(max_length=10,null = False)
    depth1 = models.CharField(max_length=20,null = False)
    depth2 = models.CharField(max_length=20,null = False)
    depth3 = models.CharField(max_length=20)
    depth4 = models.CharField(max_length=20)
    pubDate = models.DateField(null = False)
    categoryName = models.CharField(max_length=50,null = False)
    
    class Meta:
        managed = False
        db_table = 'book'
        
class LikeBook(models.Model):
    like_bookNum = models.AutoField(primary_key=True)
    userNum_like_book= models.ForeignKey(User,on_delete=models.CASCADE)
    isbn13_like_book = models.ForeignKey(Book,on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'like_book'