# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 08:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('takai', '0003_auto_20180411_0831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='theclass',
            new_name='thesession',
        ),
    ]
