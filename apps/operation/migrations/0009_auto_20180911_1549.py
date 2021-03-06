# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-11 15:49
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20180911_1549'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0008_auto_20180905_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='参与时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.ProjectShow', verbose_name='用户参与的项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.AlterField(
            model_name='usererrorchoice',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '未修改'), (2, '已修改')], default=1, verbose_name='错误题状态'),
        ),
    ]
