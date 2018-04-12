# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('cid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Classes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Enroll',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Host',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Mentor',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Mentorsessions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=255)),
                ('day', models.CharField(max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Mentorsessions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Professors',
            fields=[
                ('fid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('office', models.CharField(max_length=255)),
                ('officehours', models.CharField(blank=True, db_column='officeHours', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Professors',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('classroom', models.CharField(max_length=255)),
                ('times', models.CharField(max_length=255)),
                ('theclass', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Classes')),
            ],
            options={
                'db_table': 'Session',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('gradyear', models.TextField(db_column='gradYear')),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Students',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=1500, null=True)),
                ('picture', models.CharField(blank=True, max_length=300, null=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Students')),
            ],
            options={
                'db_table': 'TA',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Teach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Professors')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Session')),
            ],
            options={
                'db_table': 'Teach',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='mentorsessions',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Session'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Session'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Ta'),
        ),
        migrations.AddField(
            model_name='host',
            name='mentorsesh',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Mentorsessions'),
        ),
        migrations.AddField(
            model_name='host',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Session'),
        ),
        migrations.AddField(
            model_name='host',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Students'),
        ),
        migrations.AddField(
            model_name='enroll',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Session'),
        ),
        migrations.AddField(
            model_name='enroll',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Students'),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('theclass', 'semester', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='mentorsessions',
            unique_together=set([('session', 'time', 'day', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='mentor',
            unique_together=set([('student', 'session')]),
        ),
        migrations.AlterUniqueTogether(
            name='enroll',
            unique_together=set([('student', 'session')]),
        ),
    ]
