# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from users.models import UserProfile
from courses.models import Lesson

# Create your models here.


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=30, verbose_name="标签名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Catagory(models.Model):
    name = models.CharField(max_length=30, verbose_name="分类名称")
    index = models.IntegerField(default=999, verbose_name="分类的排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def get_post_nums(self):
        return self.article_set.all().count()

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    '''文章模型'''
    title = models.CharField(max_length=50, verbose_name="文章标题")
    desc = models.CharField(max_length=128, verbose_name="文章描述")
    content = UEditorField(verbose_name='文章内容', width=900, height=300, imagePath="article/ueditor/image/",
                           filePath="article/ueditor/file/", default="")
    image = models.ImageField(upload_to="post/%Y/%m", max_length=200, default="post/default.png", verbose_name="封面图")
    click_count = models.IntegerField(default=0, verbose_name="点击次数")

    fav_num = models.IntegerField(default=0, verbose_name="收藏次数")

    # view_num = GenericRelation(ViewNum)
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐")
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='作者', null=True)
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE, blank=True, null=True, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    is_reproduce = models.BooleanField(default=False, verbose_name="是否转载")
    reproduce_user = models.CharField(max_length=20, null=True, blank=True, default="", verbose_name="转载作者")
    reproduce_url = models.URLField(max_length=100, null=True, blank=True, default="", verbose_name="转载链接")
    #bb 增加关卡外键
    lesson = models.ForeignKey(Lesson, blank=True, null=True, verbose_name='所属关卡')
    no = models.IntegerField(default=0, verbose_name='关卡中的文章序号')

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


