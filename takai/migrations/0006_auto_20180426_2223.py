# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-26 22:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takai', '0005_auto_20180426_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='student',
        ),
        migrations.RemoveField(
            model_name='classinterest',
            name='interestcode',
        ),
        migrations.RemoveField(
            model_name='classinterest',
            name='session',
        ),
        migrations.RemoveField(
            model_name='classinterest',
            name='student',
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='Classinterest',
        ),
        migrations.DeleteModel(
            name='Interestcode',
        ),
    ]
