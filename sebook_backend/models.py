# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Book(models.Model):
    isbn13 = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(max_length=200)
    author = models.TextField()
    cover = models.TextField()
    categoryid = models.IntegerField(db_column='categoryId')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=30)
    malltype = models.CharField(db_column='mallType', max_length=10)  # Field name made lowercase.
    pricestandard = models.IntegerField(db_column='priceStandard')  # Field name made lowercase.
    link = models.TextField()
    adult = models.CharField(max_length=10)
    depth1 = models.CharField(max_length=20)
    depth2 = models.CharField(max_length=20)
    depth3 = models.CharField(max_length=20, blank=True, null=True)
    depth4 = models.CharField(max_length=20, blank=True, null=True)
    pubdate = models.DateField(db_column='pubDate')  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'


class BookBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    isbn13 = models.CharField(max_length=13)
    title = models.CharField(max_length=200)
    author = models.TextField()
    cover = models.TextField()
    categoryid = models.IntegerField(db_column='categoryId')  # Field name made lowercase.
    description = models.TextField()
    publisher = models.CharField(max_length=30)
    malltype = models.CharField(db_column='mallType', max_length=10)  # Field name made lowercase.
    pricestandard = models.IntegerField(db_column='priceStandard')  # Field name made lowercase.
    link = models.TextField()
    adult = models.CharField(max_length=10)
    depth1 = models.CharField(max_length=20)
    depth2 = models.CharField(max_length=20)
    depth3 = models.CharField(max_length=20)
    depth4 = models.CharField(max_length=20)
    pubdate = models.DateField(db_column='pubDate')  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_book'


class Bookreport(models.Model):
    reportnum = models.AutoField(db_column='reportNum', primary_key=True)  # Field name made lowercase.
    usernum_report = models.ForeignKey('User', models.DO_NOTHING, db_column='userNum_report')  # Field name made lowercase.
    reportcontents = models.TextField(db_column='reportContents')  # Field name made lowercase.
    reporttitle = models.TextField(db_column='reportTitle')  # Field name made lowercase.
    isbn13_report = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13_report')

    class Meta:
        managed = False
        db_table = 'bookreport'


class Community(models.Model):
    postnum = models.AutoField(db_column='postNum', primary_key=True)  # Field name made lowercase.
    contents = models.TextField()
    usernum_community = models.ForeignKey('User', models.DO_NOTHING, db_column='userNum_community')  # Field name made lowercase.
    isbn13_community = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13_community')

    class Meta:
        managed = False
        db_table = 'community'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LikeBook(models.Model):
    like_booknum = models.AutoField(db_column='like_BookNum', primary_key=True)  # Field name made lowercase.
    usernum_like_book = models.ForeignKey('User', models.DO_NOTHING, db_column='userNum_like_book')  # Field name made lowercase.
    isbn13_like_book = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn13_like_book')

    class Meta:
        managed = False
        db_table = 'like_book'


class LikeBookreport(models.Model):
    like_bookreportnum = models.AutoField(db_column='like_bookreportNum', primary_key=True)  # Field name made lowercase.
    usernum_like_bookreport = models.ForeignKey('User', models.DO_NOTHING, db_column='userNum_like_bookreport')  # Field name made lowercase.
    reportnum_like_bookreport = models.ForeignKey(Bookreport, models.DO_NOTHING, db_column='reportNum_like_bookreport')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'like_bookreport'


class LikeCommunity(models.Model):
    like_communitynum = models.AutoField(db_column='like_communityNum', primary_key=True)  # Field name made lowercase.
    usernum_like_community = models.ForeignKey('User', models.DO_NOTHING, db_column='userNum_like_community')  # Field name made lowercase.
    postnum_like_community = models.ForeignKey(Community, models.DO_NOTHING, db_column='postNum_like_community')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'like_community'


class User(models.Model):
    usernum = models.AutoField(db_column='userNum', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='userId', max_length=45)  # Field name made lowercase.
    password = models.CharField(max_length=45)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'user'
