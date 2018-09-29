# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-16 09:14
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户课程',
                'verbose_name_plural': '用户课程',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='接收用户')),
                ('message', models.CharField(max_length=500, verbose_name='消息内容')),
                ('has_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户消息',
                'verbose_name_plural': '用户消息',
            },
        ),
        migrations.CreateModel(
            name='UserQuestionTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_content', DjangoUeditor.models.UEditorField(verbose_name='提问内容')),
                ('answer', DjangoUeditor.models.UEditorField(verbose_name='老师回答')),
                ('question_status', models.IntegerField(choices=[(1, '已回答'), (0, '未回答')], default=0, verbose_name='是否已经回答')),
                ('user_question_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='提问时间')),
                ('teacher_answer_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='回答时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='提问用户')),
            ],
            options={
                'verbose_name': '用户问题回答',
                'verbose_name_plural': '用户问题回答',
            },
        ),
    ]