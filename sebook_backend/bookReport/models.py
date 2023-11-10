from django.db import models
from user.models import User
from book.models import Book
from django.utils import timezone
# Create your models here.

class BookReport(models.Model):
    reportNum = models.AutoField(primary_key=True, null=False)
    userNum_report = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userNum_report')
    reportContents = models.TextField(null=False)
    reportTitle = models.TextField(null=False)
    registDate_report = models.DateTimeField(null=False)
    isbn13_report = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn13_report')

    def save(self, *args, **kwargs):
        if not self.pk:  # 새로운 모델 인스턴스인 경우에만 시간 설정
            self.registDate_report = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'bookreport'

class LikeBookReport(models.Model):
    like_bookreportNum = models.AutoField(primary_key=True)
    userNum_like_bookreport = models.ForeignKey(User,on_delete=models.CASCADE, db_column='userNum_like_bookreport')
    reportNum_like_bookreport = models.ForeignKey(BookReport,on_delete=models.CASCADE,db_column='reportNum_like_bookreport')
    class Meta:
        managed = False
        db_table = 'like_bookreport'
        
