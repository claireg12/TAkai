# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Classes(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'Classes'

# Added primary key ???
class Enroll(models.Model):
    sid = models.ForeignKey('Students', models.DO_NOTHING, db_column='sid', blank=False, null=False, related_name='sid_enroll_set', primary_key=True)
    cid = models.ForeignKey('Session', models.DO_NOTHING, db_column='cid', blank=False, null=False, related_name='cid_enroll_set')
    semester = models.ForeignKey('Session', models.DO_NOTHING, db_column='semester', blank=False, null=False, related_name='semester_enroll_set')
    year = models.ForeignKey('Session', models.DO_NOTHING, db_column='year', blank=False, null=False, related_name='year_enroll_set')

    class Meta:
        managed = False
        db_table = 'Enroll'

# Added primary key ???
class Mentor(models.Model):
    sid = models.ForeignKey('Students', models.DO_NOTHING, db_column='sid', blank=False, null=False, related_name='sid_mentor_set', primary_key=True)
    cid = models.ForeignKey('Session', models.DO_NOTHING, db_column='cid', blank=False, null=False, related_name='cid_mentor_set')
    semester = models.ForeignKey('Session', models.DO_NOTHING, db_column='semester', blank=False, null=False, related_name='semester_mentor_set')
    year = models.ForeignKey('Session', models.DO_NOTHING, db_column='year', blank=False, null=False, related_name='year_mentor_set')

    class Meta:
        managed = False
        db_table = 'Mentor'


class Mentorsessions(models.Model):
    cid = models.ForeignKey('Session', models.DO_NOTHING, db_column='cid', blank=False, null=False, related_name='cid_mentorsessions_set')
    semester = models.ForeignKey('Session', models.DO_NOTHING, db_column='semester', blank=False, null=False, related_name='semester_mentorsessions_set')
    year = models.ForeignKey('Session', models.DO_NOTHING, db_column='year', blank=False, null=False, related_name='year_mentorsessions_set')
    time = models.CharField(primary_key=True, max_length=255)
    day = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Mentorsessions'


class Professors(models.Model):
    fid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    office = models.CharField(max_length=255, blank=False, null=False)
    officehours = models.CharField(db_column='officeHours', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professors'


class Session(models.Model):
    cid = models.ForeignKey(Classes, models.DO_NOTHING, db_column='cid', primary_key=True)
    semester = models.CharField(max_length=50)
    year = models.TextField()  # This field type is a guess.
    classroom = models.CharField(max_length=255, blank=False, null=False)
    times = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'Session'
        unique_together = (('cid', 'semester', 'year'),)


class Students(models.Model):
    sid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    gradyear = models.TextField(db_column='gradYear', blank=False, null=False)  # Field name made lowercase. This field type is a guess.
    email = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'Students'

# Added primary key????
class Ta(models.Model):
    sid = models.ForeignKey(Students, models.DO_NOTHING, db_column='sid', blank=False, null=False, primary_key=True)
    bio = models.CharField(max_length=1500, blank=True, null=True)
    picture = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TA'

class Teach(models.Model):
    fid = models.ForeignKey(Professors, models.DO_NOTHING, db_column='fid', blank=True, null=False, related_name='fid_teach_set')
    cid = models.ForeignKey(Session, models.DO_NOTHING, db_column='cid', blank=True, null=False, related_name='cid_teach_set', primary_key=True)
    semester = models.ForeignKey(Session, models.DO_NOTHING, db_column='semester', blank=False, null=True, related_name='semester_teach_set')
    year = models.ForeignKey(Session, models.DO_NOTHING, db_column='year', blank=True, null=False, related_name='year_teach_set')

    class Meta:
        managed = False
        db_table = 'Teach'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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
