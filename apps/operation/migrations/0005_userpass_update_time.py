# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-21 11:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_auto_20180818_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpass',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='状态更新时间'),
        ),
    ]
