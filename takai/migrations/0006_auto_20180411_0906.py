# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('takai', '0005_auto_20180411_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='takai.Ta'),
        ),
    ]
