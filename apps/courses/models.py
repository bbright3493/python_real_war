# _*_ encoding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models
from DjangoUeditor.models import UEditorField
from datetime import datetime

from users.models import UserProfile


# Create your models here.


class CourseDirection(models.Model):
    """
    课程方向
    """
    direction = models.CharField(max_length=36, verbose_name="课程方向")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "课程方向"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.direction


class CourseCategory(models.Model):
    """
    课程分类
    """
    # coursedirection = models.ForeignKey(CourseDirection, verbose_name="课程方向", default="")
    category = models.CharField(max_length=36, verbose_name="课程分类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "课程分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField(verbose_name=u"难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"建议学习时长")
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"课程封面", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    # category = models.CharField(default=u"后端开发", max_length=20, verbose_name=u"课程类别", null=True, blank=True)
    coursecategory = models.ForeignKey(CourseCategory, verbose_name="课程分类", default="")
    diretion_choices = (
        ("base", "基础课程"),
        ("project", "项目课程"),
    )
    direction = models.CharField(choices=diretion_choices, max_length=10, default="base", verbose_name="课程方向")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name=u"课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name=u"老师告诉你")

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    # get_zj_nums.short_description = "章节数"

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    课程关卡
    """
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"关卡名")
    image = models.ImageField(max_length=128, default="", verbose_name="关卡图")
    learn_times = models.IntegerField(default=0, verbose_name=u"建议完成时长")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    learn_require = models.CharField(max_length=300, verbose_name=u"关卡学习要求")
    learn_target = models.CharField(max_length=300, verbose_name=u"关卡学习目标")
    resource = models.CharField(max_length=300, verbose_name=u"关卡学习资源网盘地址")
    tutorial = models.CharField(max_length=200, default="", verbose_name=u"关卡教程地址")
    opt_require = models.CharField(max_length=300, verbose_name=u"关卡实操要求")
    ext_resource = models.CharField(max_length=300, verbose_name=u"关卡扩展资源网盘地址")
#    choice_detail = models.CharField(max_length=100, verbose_name="选择题描述", default="")
#    program_detail = models.CharField(max_length=100, verbose_name="编程题描述", default="")
    # open_level = models.BooleanField(default=False, verbose_name="开通关卡")
    # pass_level = models.BooleanField(default=False, verbose_name="通过关卡")

    class Meta:
        verbose_name = u"课程关卡"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()

    def get_program_id(self):
        return self.programquestion_set.first()

    def get_choice_bank(self):
        # 获取选择题库
        return self.choicebank_set.first()

    def get_program_bank(self):
        # 获取编程题库
        return self.programbank_set.first()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(default=0, verbose_name=u"视频时长(分钟数)")
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Faq(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡")
    question = models.CharField(max_length=500, verbose_name=u"问题")
    answer = models.CharField(max_length=1500, verbose_name=u"回答")

    class Meta:
        verbose_name = u"FAQ"
        verbose_name_plural = verbose_name


# class QuestionBank(models.Model):
#     """
#     题库
#     """
#     lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡")
#     name = models.CharField(max_length=100, verbose_name=u'题库名称')
#     desc = models.CharField(max_length=200, verbose_name=u'题库描述', null=True, blank=True)
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
#     click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
#     degree = models.CharField(verbose_name=u"难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2,
#                               null=True, blank=True)
#     complete_times = models.IntegerField(default=0, verbose_name=u"建议完成时长(分钟数)")
#     image = models.ImageField(upload_to="onlinepractice/%Y/%m", verbose_name=u"封面图", max_length=100, null=True,
#                               blank=True)
#     fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
#     type = models.CharField(verbose_name=u"题库类别", choices=(("xzt", "选择题"), ("bct", "编程题")), max_length=5, null=True,
#                             blank=True)
#     detail = models.CharField(max_length=300, verbose_name=u'题库详情', null=True, blank=True)
#
#     class Meta:
#         verbose_name = u'题库'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class ChoiceBank(models.Model):
    """
    选择题题库
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡", default="")
    name = models.CharField(max_length=100, verbose_name=u'题库名称')
    desc = models.CharField(max_length=200, verbose_name=u'题库描述', null=True, blank=True)

    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    complete_times = models.IntegerField(default=0, verbose_name=u"建议完成时长(分钟数)")
    is_complete = models.BooleanField(default=False, verbose_name="是否完成")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'选择题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ChoiceQuestion(models.Model):
    """
    选择题表
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡", default="")
    choicebank = models.ForeignKey(ChoiceBank, verbose_name="选择题库", default="")
    question_num = models.IntegerField(verbose_name=u'题目编号')
    question_content = models.CharField(max_length=500, verbose_name=u'题目内容')
    choiceA = models.CharField(max_length=200, verbose_name=u'选项A')
    choiceB = models.CharField(max_length=200, verbose_name=u'选项B')
    choiceC = models.CharField(max_length=200, verbose_name=u'选项C')
    choiceD = models.CharField(max_length=200, verbose_name=u'选项D')
    answer_choices = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
    )
    answer = models.SmallIntegerField(choices=answer_choices, verbose_name=u'答案', default=0)
    explain = models.TextField(verbose_name=u'答案解释')

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'选择题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s 第%d题"%(self.lesson.name, self.question_num)



class ProgramBank(models.Model):
    """
    实操题库
    """
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡", default="")
    name = models.CharField(max_length=100, verbose_name=u'题库名称')
    desc = models.CharField(max_length=200, verbose_name=u'题库描述', null=True, blank=True)

    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    complete_times = models.IntegerField(default=0, verbose_name=u"建议完成时长(分钟数)")
    is_complete = models.BooleanField(default=False, verbose_name="是否完成")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'实操题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProgramQuestion(models.Model):
    """
    编程题表
    """

    program_types = (
        (1, "课堂练习"),
        (2, "课后扩展"),
    )
    program_type = models.SmallIntegerField(choices=program_types, verbose_name=u'编程题类型', default=1)
    lesson = models.ForeignKey(Lesson, verbose_name=u"课程关卡", default="")
    program_bank = models.ForeignKey(ProgramBank, verbose_name=u"实操题库", default="")
    question_num = models.IntegerField(verbose_name=u'题目编号')
    question_title = models.CharField(max_length=36, default="", verbose_name="编程题目")
    question_content = models.TextField(verbose_name=u'题目内容')
    download = models.FileField(upload_to="program/download/%Y/%m", verbose_name=u"源码文件", max_length=100, default='')
    url = models.CharField(max_length=200, default="", verbose_name=u"题目讲解视频地址")
    essentials = models.CharField(max_length=2000, verbose_name=u'解题思路')
    image = models.ImageField(upload_to="program/image/%Y/%m", verbose_name=u"运行结果截图", max_length=100, null=True,
                              blank=True)
    is_comment = models.BooleanField(default=False, verbose_name=u'是否提供点评')
    is_complete = models.BooleanField(default=False, verbose_name="是否完成")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    result = models.CharField(default='', max_length=2000, verbose_name='代码运行结果')

    class Meta:
        verbose_name = u'编程题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question_title


class ProgramUpload(models.Model):
    """
    编程题结果上传
    """
    lesson = models.ForeignKey(Lesson, default="", verbose_name="关卡")
    programquestion = models.ForeignKey(ProgramQuestion, verbose_name="编程题", null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name="用户", null=True, blank=True)
    upload = models.FileField(upload_to="program/upload/file/%Y/%m", verbose_name=u"源码文件", max_length=100, default='',
                              null=True, blank=True)
    image = models.ImageField(upload_to="program/upload/image/%Y/%m", verbose_name=u"运行结果截图", max_length=100, null=True,
                              blank=True)
    grade_choices = (
        ("优秀", "A+"),
        ("优良", "A"),
        ("良好", "B"),
        ("及格", "C"),
        ("不及格", "D")
    )
    grade = models.CharField(max_length=5, choices=grade_choices, verbose_name="等级", null=True, blank=True)
    learned = models.TextField(verbose_name="练习心得", default="", null=True, blank=True)
    comment = models.TextField(verbose_name="项目点评", default="", null=True, blank=True)
    is_complete = models.BooleanField(default=False, verbose_name="是否完成")
    is_show = models.BooleanField(default=False, verbose_name="是否展示")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'编程题结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.programquestion.question_title


class ProgramResultImg(models.Model):
    """
    项目运行截图
    """
    programupload = models.ForeignKey(ProgramUpload, verbose_name="编程题结果")
    image = models.ImageField(max_length=100, verbose_name="运行截图")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "项目运行截图"
        verbose_name_plural = verbose_name

    # def __unicode__(self):
    #     return
