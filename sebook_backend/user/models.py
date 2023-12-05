from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserManager(BaseUserManager):
    def create_user(self, userId, password=None, **extra_fields):
        if not userId:
            raise ValueError('The User ID field must be set')
        user = self.model(userId=userId, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(userId, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    userNum = models.AutoField(primary_key=True, null=False)
    userId = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=20, null=False)
    last_login = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'userId'

    class Meta:
        db_table = 'user'