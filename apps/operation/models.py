# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

from users.models import UserProfile
from courses.models import Course, ChoiceQuestion, Lesson
from article.models import Article

from project.models import ProjectShow


# Create your models here.
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserQuestionTeacher(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"提问用户")
    question_content = UEditorField(verbose_name=u"提问内容", width=600, height=300, imagePath="operation/ueditor/",
                                    filePath="operation/ueditor/")
    answer = UEditorField(verbose_name=u"老师回答", width=600, height=300, imagePath="operation/ueditor/",
                          filePath="operation/ueditor/")
    question_status = models.IntegerField(choices=((1, "已回答"), (0, "未回答")), default=0, verbose_name=u'是否已经回答')
    user_question_time = models.DateTimeField(default=datetime.now, verbose_name=u"提问时间")
    teacher_answer_time = models.DateTimeField(default=datetime.now, verbose_name=u"回答时间")

    class Meta:
        verbose_name = u'用户问题回答'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    '''用户课程'''
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    stu_status = (
        (1, "未学习"),
        (2, "学习中"),
        (3, "已学习"),
    )
    study_status = models.SmallIntegerField(choices=stu_status, verbose_name=u'课程的学习状态', default=1)

    cour_status = (
        (1, "未开通"),
        (2, "已开通"),
    )

    course_status = models.SmallIntegerField(choices=cour_status, verbose_name=u'课程状态', default=1)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s--%s" % (self.user.username, self.course.name)


class UserPass(models.Model):
    """
    用户关卡信息
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    lesson = models.ForeignKey(Lesson, verbose_name="关卡")
    lesson_status = (
        (1, "未开通"),
        (2, "已开通"),
    )
    study_status = (
        (1, "未学习"),
        (2, "学习中"),
        (3, "已学习")
    )
    status = models.SmallIntegerField(choices=lesson_status, verbose_name=u'关卡状态', default=1)
    lesson_study_status = models.SmallIntegerField(choices=study_status, verbose_name=u'关卡学习状态', default=1)
    # 0表示还没有提交过选择题 1表示提交过一次 如果是第一次提交并且已经开通关卡或者课程权限 则需要保存做错的题目
    choice_status = models.SmallIntegerField(verbose_name=u'关卡选择题库答题状态', default=0)

    update_time = models.DateTimeField(default=datetime.now, verbose_name=u"状态更新时间")
    class Meta:
        verbose_name = "用户关卡信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.user.username, self.lesson.name)


class UserErrorChoice(models.Model):
    """
    用户错误选择题表
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    choice = models.ForeignKey(ChoiceQuestion, verbose_name="做错的选择题")
    answer_choices = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
    )
    user_answer = models.SmallIntegerField(choices=answer_choices, verbose_name=u'用户的错误答案', default=0)
    error_time = models.DateTimeField(default=datetime.now, verbose_name=u"做题时间")
    answer_status = (
        (1, "未修改"),
        (2, "已修改"),
    )
    status = models.SmallIntegerField(choices=answer_status, verbose_name=u'错误题状态', default=1)

    class Meta:
        verbose_name = "用户错误选择题"
        verbose_name_plural = verbose_name


class UserFavArticle(models.Model):
    """
    用户收藏文章表
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    article_id = models.IntegerField(default=0, verbose_name=u"文章id")


    class Meta:
        verbose_name = "用户收藏文章"
        verbose_name_plural = verbose_name


class UserProject(models.Model):
    """
    用户项目表
    """
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    project = models.ForeignKey(ProjectShow, verbose_name="用户参与的项目")
    join_time = models.DateTimeField(default=datetime.now, verbose_name=u"参与时间")


