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

    def __str__(self):
        return str(self.cid)

    class Meta:
        managed = True
        db_table = 'Classes'

class Mentor(models.Model):
    ta = models.ForeignKey('Ta', on_delete=models.CASCADE, blank=False, null=False) # should be renamed to ta
    session = models.ForeignKey('Session', on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.ta.student.name) + ' ' + str(self.session)

    class Meta:
        managed = True
        db_table = 'Mentor'
        unique_together = (('ta', 'session'),)


class Mentorsessions(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, blank=False, null=False)
    time = models.CharField(max_length=255) # removed primary key
    day = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.session) + ' ' + str(self.time) + ' ' + str(self.day)

    class Meta:
        managed = True
        db_table = 'Mentorsessions'
        unique_together = (('session', 'time','day','location'),)

class Enroll(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE, blank=False, null=False)
    session = models.ForeignKey('Session', on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'Enroll'
        unique_together = (('student','session'),)

    def __str__(self):
        return str(self.student.sid) + ' ' + str(self.session.theclass.cid)


class Professors(models.Model):
    fid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    office = models.CharField(max_length=255, blank=False, null=False)
    officehours = models.CharField(db_column='officeHours', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return ' ' + str(self.name) + ' ' + str(self.fid) + ' ' + str(self.email)

    class Meta:
        managed = True
        db_table = 'Professors'


class Session(models.Model):
    theclass = models.ForeignKey(Classes, on_delete=models.CASCADE)
    semester = models.CharField(max_length=255,blank=False, null=False)
    year = models.CharField(max_length=255, blank=False, null=False)
    classroom = models.CharField(max_length=255, blank=False, null=False)
    times = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return ' ' + str(self.theclass) + ' ' + str(self.year) + ' ' + str(self.semester)

    class Meta:
        managed = True
        db_table = 'Session'
        unique_together = (('theclass', 'semester', 'year'),)


class Students(models.Model):
    sid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    gradyear = models.TextField(db_column='gradYear', blank=False, null=False)  # Field name made lowercase. This field type is a guess.
    email = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        managed = True
        db_table = 'Students'

class Ta(models.Model):
    student = models.OneToOneField(Students, on_delete=models.CASCADE, blank=False, null=False) # from pk to one to one field
    bio = models.CharField(max_length=1500, blank=True, null=True)
    picture = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.student.name)

    class Meta:
        managed = True
        db_table = 'TA'

class Teach(models.Model):
    professor = models.ForeignKey(Professors, on_delete=models.CASCADE, blank=False, null=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.professor) + ' ' + str(self.session)

    class Meta:
        managed = True
        db_table = 'Teach'

class Host(models.Model):
    ta = models.ForeignKey(Ta, on_delete=models.CASCADE, blank=False, null=False) # should be mentor
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=False, null=False)
    mentorsesh = models.ForeignKey(Mentorsessions, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return str(self.ta.student.name) + ' ' + str(self.session) + ' ' + str(self.mentorsesh.time) + ' ' + str(self.mentorsesh.day)

    class Meta:
        managed = True
        db_table = 'Host'

class Application(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)
    semester = models.CharField(max_length=255,blank=False, null=False)
    year = models.CharField(max_length=255, blank=False, null=False)
    school = models.CharField(max_length=50, blank=False, null=False)
    major = models.CharField(max_length=100, blank=False, null=False)
    qualities = models.CharField(max_length=1500, blank=False, null=False)
    num_hours_week = models.FloatField()

    def __str__(self):
        return str(self.semester) + ' ' + str(self.year) + ' ' + str(self.school) + ' ' + str(self.major) + ' ' + str(self.qualities) + ' ' + str(self.num_hours_week)

    class Meta:
        managed = True
        db_table = 'Application'

class Availabilitycode(models.Model):
    code = models.IntegerField(primary_key=True)
    meaning = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return str(self.meaning)

    class Meta:
        managed = True
        db_table = 'Availabilitycode'

class Availability(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)
    availabilitycode = models.ForeignKey(Availabilitycode, models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return str(self.availabilitycode.meaning)

    class Meta:
        managed = True
        db_table = 'Availability'

class Interestcode(models.Model):
    code = models.IntegerField(primary_key=True)
    meaning = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return str(self.meaning)

    class Meta:
        managed = True
        db_table = 'Interestcode'

class Classinterest(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, blank=False, null=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=False, null=False)
    interestcode = models.ForeignKey(Interestcode, models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return str(self.session.theclass.cid) + ' ' + str(self.interestcode.meaning)

    class Meta:
        managed = True
        db_table = 'Classinterest'


# CREATE TABLE InterestCode(code int, meaning char (100))
# CREATE TABLE ClassInterest(student int, session , interestcode int)


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
