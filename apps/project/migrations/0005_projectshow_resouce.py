# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-13 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20180913_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectshow',
            name='resouce',
            field=models.FileField(blank=True, default='', max_length=128, null=True, upload_to='project/show/files/%Y/%m', verbose_name='项目素材'),
        ),
    ]
