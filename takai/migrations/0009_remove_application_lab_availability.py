# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-29 22:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takai', '0008_auto_20180427_0702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='lab_availability',
        ),
    ]
