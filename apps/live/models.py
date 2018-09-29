# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from users.models import UserProfile

# Create your models here.


class LivePreview(models.Model):
    """
    直播预告
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    title = models.CharField(max_length=36, verbose_name="标题")
    content = UEditorField(verbose_name="直播内容", width=900, height=300, imagePath="live/ueditor/image/",
                           filePath="live/ueditor/file/", default="")
    live_time = models.DateTimeField(verbose_name="直播时间", default=datetime.now)
    link = models.URLField(max_length=128, verbose_name="直播链接")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "直播预告"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
