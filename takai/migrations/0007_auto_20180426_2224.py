# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-26 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('takai', '0006_auto_20180426_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=50)),
                ('major', models.CharField(max_length=100)),
                ('qualities', models.CharField(max_length=1500)),
                ('num_hours_week', models.FloatField()),
                ('lab_availability', models.CharField(max_length=100)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takai.Students')),
            ],
            options={
                'db_table': 'Application',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Classinterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Classinterest',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Interestcode',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('meaning', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Interestcode',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='classinterest',
            name='interestcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Interestcode'),
        ),
        migrations.AddField(
            model_name='classinterest',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takai.Session'),
        ),
        migrations.AddField(
            model_name='classinterest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='takai.Students'),
        ),
    ]