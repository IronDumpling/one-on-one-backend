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
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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


class MeetingsCalendar(models.Model):
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    meeting = models.ForeignKey('MeetingsMeeting', models.DO_NOTHING)
    owner = models.ForeignKey('MeetingsMember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_calendar'


class MeetingsEvent(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    availability = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    calendar = models.ForeignKey(MeetingsCalendar, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_event'


class MeetingsJoinnode(models.Model):
    node_ptr = models.OneToOneField('MeetingsNode', models.DO_NOTHING, primary_key=True)
    receiver = models.ForeignKey('MeetingsMember', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_joinnode'


class MeetingsMeeting(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=20)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meetings_meeting'


class MeetingsMember(models.Model):
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    meeting = models.ForeignKey(MeetingsMeeting, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_member'


class MeetingsNode(models.Model):
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    meeting = models.ForeignKey(MeetingsMeeting, models.DO_NOTHING)
    sender = models.ForeignKey(MeetingsMember, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_node'


class MeetingsPollnode(models.Model):
    node_ptr = models.OneToOneField(MeetingsNode, models.DO_NOTHING, primary_key=True)
    state = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'meetings_pollnode'


class MeetingsRemindnode(models.Model):
    node_ptr = models.OneToOneField(MeetingsNode, models.DO_NOTHING, primary_key=True)
    message = models.CharField(max_length=120)
    receiver = models.ForeignKey(MeetingsMember, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meetings_remindnode'


class MeetingsStatenode(models.Model):
    node_ptr = models.OneToOneField(MeetingsNode, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'meetings_statenode'


class MeetingsSubmitnode(models.Model):
    node_ptr = models.OneToOneField(MeetingsNode, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'meetings_submitnode'
