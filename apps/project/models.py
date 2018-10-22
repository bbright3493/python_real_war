# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from courses.models import CourseCategory, Course, Lesson
from users.models import UserProfile

# Create your models here.


class ProjectShow(models.Model):
    """
    项目展示
    """
    coursecategory = models.ForeignKey(CourseCategory, verbose_name="分类")
    name = models.CharField(max_length=36, verbose_name="项目名称")
#    user = models.ForeignKey(UserProfile, verbose_name="作者")
    degree_choices = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    degree = models.CharField(verbose_name=u"难度", choices=degree_choices, max_length=2, default="")

    type = (
        (1, "随堂项目"),
        (2, "综合项目"),
        (3, "趣味项目"),
        (4, "商业项目"),
    )

    project_type = models.SmallIntegerField(choices=type, verbose_name=u'项目类型', default=1)
    #该字段只有随堂项目才有 某些配套课程的综合项目也有
    lesson = models.ForeignKey(Lesson, verbose_name="项目对应关卡", null=True, blank=True,default='')

    image = models.ImageField(upload_to="project/show/images/%Y/%m" ,max_length=128, verbose_name="项目图片")
    describe = models.CharField(max_length=128, verbose_name="项目描述")
    url = models.URLField(verbose_name="项目演示视频链接")
    video = models.CharField(max_length=200, verbose_name='讲解视频下载地址', null=True, blank=True,default='')
    code = models.FileField(upload_to="project/show/files/%Y/%m", max_length=128, verbose_name="项目源码")
    resouce = models.FileField(upload_to="project/show/files/%Y/%m", max_length=128, verbose_name="项目素材",
                               default='', null=True, blank=True)
    click_num = models.IntegerField(default=0, verbose_name="点击数")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course = models.ManyToManyField(Course, verbose_name="相关课程", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    require_file = models.FileField(upload_to="project/show/files/%Y/%m", max_length=128,
                                    verbose_name="项目需求文档", default='', null=True, blank=True)
    plan_file = models.FileField(upload_to="project/show/files/%Y/%m", max_length=128,
                                 verbose_name="项目计划文档", default='', null=True, blank=True)
    test_file =models.FileField(upload_to="project/show/files/%Y/%m", max_length=128,
                                verbose_name="项目测试说明", default='', null=True, blank=True)

    integral = models.IntegerField(default=0, verbose_name="参与项目所需积分")

    tag = models.CharField(max_length=500, verbose_name="项目标签", null=True, blank=True, default='')


    class Meta:
        verbose_name = "项目展示"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name