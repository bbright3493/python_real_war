# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Lesson


# Create your models here.


class UserIntergral(models.Model):
    """
    用户积分信息表
    """
    user = models.OneToOneField(UserProfile, verbose_name="用户")
    grade = models.IntegerField(default=0, verbose_name="积分分数")
    sign_day = models.IntegerField(verbose_name="签到天数", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "用户积分表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class IntegralRecord(models.Model):
    """
    用户积分记录
    """
    userintergral = models.ForeignKey(UserIntergral, verbose_name="用户积分")
    gain_choices = (
        ("recharge", "充值"),
        ("task", "任务")
    )
    gain = models.CharField(max_length=10, choices=gain_choices, verbose_name="获取方式", default="task")
    detail = models.CharField(max_length=64, verbose_name="积分明细")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "积分记录表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userintergral.user.username


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    user = models.ForeignKey(UserProfile, verbose_name="用户")
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name=u"交易号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    post_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话", default='')

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"积分充值订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class IntergralDemand(models.Model):
    """积分需求"""
    lesson = models.ForeignKey(Lesson, verbose_name="课程关卡")
    intergral_choices = (
        ("extend_download", "扩展资料"),
        ("pro_explain", "项目讲解")
    )
    demand = models.CharField(choices=intergral_choices, max_length=16, verbose_name="需求")
    intergral = models.IntegerField(default=0, verbose_name="需求积分")
    url = models.URLField(verbose_name="下载链接")
    download_count = models.IntegerField(default=0, verbose_name="下载次数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "积分需求"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s--%s--%s" % (self.lesson.course.name, self.lesson.name, self.get_demand_display())
