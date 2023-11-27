# from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BackendLanguage(models.Model):
    backend_no = models.AutoField(db_column='BACKEND_NO', primary_key=True)  # Field name made lowercase.
    backend_name = models.CharField(db_column='BACKEND_NAME', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Backend_Language'


class DbList(models.Model):
    db_no = models.AutoField(db_column='DB_NO', primary_key=True)  # Field name made lowercase.
    db_name = models.CharField(db_column='DB_NAME', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DB_List'


class Region(models.Model):
    region_no = models.AutoField(db_column='REGION_NO', primary_key=True)  # Field name made lowercase.
    region_code = models.CharField(db_column='REGION_CODE', max_length=255)  # Field name made lowercase.
    region_name = models.CharField(db_column='REGION_NAME', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REGION'


class Serviceaws(models.Model):
    service_no = models.AutoField(db_column='SERVICE_NO', primary_key=True)  # Field name made lowercase.
    uno = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='UNO')  # Field name made lowercase.
    region_no = models.ForeignKey(Region, models.DO_NOTHING, db_column='REGION_NO')  # Field name made lowercase.
    db_no = models.ForeignKey(DbList, models.DO_NOTHING, db_column='DB_NO')  # Field name made lowercase.
    backend_no = models.ForeignKey(BackendLanguage, models.DO_NOTHING, db_column='BACKEND_NO')  # Field name made lowercase.
    service_name = models.CharField(db_column='SERVICE_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ecr_uri = models.CharField(db_column='ECR_URI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    load_balancer_name = models.CharField(db_column='LOAD_BALANCER_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    s3_arn = models.CharField(db_column='S3_ARN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cloudfront_dns = models.CharField(db_column='CLOUDFRONT_DNS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    frontend_fl = models.CharField(db_column='FRONTEND_FL', max_length=4,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ServiceAws'


class Userinfo(models.Model):
    uno = models.AutoField(db_column='UNO', primary_key=True)  # Field name made lowercase.
    uid = models.CharField(db_column='UID', max_length=255)  # Field name made lowercase.
    upwd = models.CharField(db_column='UPWD', max_length=255)  # Field name made lowercase.
    uname = models.CharField(db_column='UNAME', max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=255)  # Field name made lowercase.
    regist_date = models.DateField(db_column='REGIST_DATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserInfo'


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

