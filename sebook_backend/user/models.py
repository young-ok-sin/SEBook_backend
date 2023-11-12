from django.db import models

# Create your models here.
class User(models.Model):
    userNum = models.AutoField(primary_key=True,null=False)
    userId = models.CharField(max_length=45, null = False)
    password = models.CharField(max_length=45, null = False)
    name = models.CharField(max_length=20, null = False)
    
    class Meta:
        managed = False
        db_table = 'user'
        
    @staticmethod
    def authenticate_user(userId, password):
        try:
            user = User.objects.get(userId=userId, password=password)
            return user.userNum
        except User.DoesNotExist:
            return None