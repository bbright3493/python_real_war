# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-13 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20180912_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectshow',
            name='video',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='讲解视频下载地址'),
        ),
        migrations.AlterField(
            model_name='projectshow',
            name='url',
            field=models.URLField(verbose_name='项目演示视频链接'),
        ),
    ]
