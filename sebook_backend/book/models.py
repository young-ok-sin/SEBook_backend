from django.db import models
from user.models import CustomUser


class Category(models.Model):
    categoryId = models.IntegerField(primary_key=True,null = False)
    depth1 = models.CharField(max_length=20, null = False)
    depth2 = models.CharField(max_length=20, null = False)
    depth3 = models.CharField(max_length=20)
    depth4 = models.CharField(max_length=20)
    
    class Meta:
        managed = False
        db_table = 'category'

class Book(models.Model):
    isbn13 = models.CharField(max_length=13, primary_key=True, null=False)
    title = models.CharField(max_length=200, null=False)
    author = models.TextField(null=False)
    cover = models.TextField(null=False)
    categoryId_book = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='categoryId_book')
    description = models.TextField()
    publisher = models.CharField(max_length=30, null=False)
    mallType = models.CharField(max_length=10, null=False)
    priceStandard = models.IntegerField(null=False)
    link = models.TextField(null=False)
    adult = models.CharField(max_length=10, null=False)
    pubDate = models.DateField(null=False)
    categoryName = models.CharField(max_length=50, null=False)
    num_likes = models.IntegerField(null=False, default=0)  # 좋아요 수 필드

    class Meta:
        managed = False
        db_table = 'book'
        indexes = [
            models.Index(fields=['num_likes']),  # num_likes 필드에 인덱스 추가
        ]
        
class LikeBook(models.Model):
    like_bookNum = models.AutoField(primary_key=True)
    userNum_like_book= models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='userNum_like_book')
    isbn13_like_book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn13_like_book')
    
    class Meta:
        managed = False
        db_table = 'like_book'
#----------------------------------------------------------------------------------
# from django.db import models
# from user.models import User


# class Book(models.Model):
#     isbn13 = models.CharField(max_length=13,primary_key=True,null = False)
#     title = models.CharField(max_length=200, null = False)
#     author = models.TextField(null = False)
#     cover = models.TextField(null = False)
#     categoryId_book = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='categoryId_book')
#     description = models.TextField()
#     publisher = models.CharField(max_length=30,null = False)
#     mallType = models.CharField(max_length=10,null = False)
#     priceStandard = models.IntegerField(null = False)
#     link = models.TextField(null = False)
#     adult = models.CharField(max_length=10,null = False)
#     pubDate = models.DateField(null = False)
#     categoryName = models.CharField(max_length=50,null = False)
    
#     class Meta:
#         managed = False
#         db_table = 'book'
        
# class LikeBook(models.Model):
#     like_bookNum = models.AutoField(primary_key=True)
#     userNum_like_book= models.ForeignKey(User, on_delete=models.CASCADE, db_column='userNum_like_book')
#     isbn13_like_book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn13_like_book')
    
#     class Meta:
#         managed = False
#         db_table = 'like_book'
        

