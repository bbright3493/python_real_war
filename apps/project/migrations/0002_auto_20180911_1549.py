# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-11 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectshow',
            name='plan_file',
            field=models.FileField(default='', max_length=128, upload_to='project/show/files/%Y/%m', verbose_name='项目计划文档'),
        ),
        migrations.AddField(
            model_name='projectshow',
            name='require_file',
            field=models.FileField(default='', max_length=128, upload_to='project/show/files/%Y/%m', verbose_name='项目需求文档'),
        ),
        migrations.AddField(
            model_name='projectshow',
            name='test_file',
            field=models.FileField(default='', max_length=128, upload_to='project/show/files/%Y/%m', verbose_name='项目测试说明'),
        ),
    ]
