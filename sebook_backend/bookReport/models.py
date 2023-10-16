from django.db import models
from user.models import User
from book.models import Book
# Create your models here.

class BookReport(models.Model):
    reportNum = models.AutoField(primary_key=True,null = False)
    userNum_report = models.ForeignKey(User,on_delete=models.CASCADE)
    reportContents = models.TextField(null = False)
    reportTitle = models.TextField(null = False)
    isbn13_report = models.ForeignKey(Book,on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'bookreport'

class LikeBookReport(models.Model):
    like_bookreportNum = models.AutoField(primary_key=True)
    userNum_like_bookreport = models.ForeignKey(User,on_delete=models.CASCADE)
    reportNum_like_bookrepor = models.ForeignKey(BookReport,on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'like_bookreport'