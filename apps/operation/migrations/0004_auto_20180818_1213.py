# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-18 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_usercourse_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpass',
            name='lesson_study_status',
            field=models.SmallIntegerField(choices=[(1, '未学习'), (2, '学习中'), (3, '已学习')], default=1, verbose_name='关卡学习状态'),
        ),
        migrations.AlterField(
            model_name='userpass',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '未开通'), (2, '已开通')], default=1, verbose_name='关卡状态'),
        ),
    ]
