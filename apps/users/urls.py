#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-10 上午9:53
# @Author  : Ztsong

from django.conf.urls import url

from .views import UserInfoView, UserModifyView, ModifyPwdView

urlpatterns = [
    # 个人中心
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    # 个人信息修改
    url(r'^modify/info/$', UserModifyView.as_view(), name="modify_info"),
    # 密码修改
    url(r'^modify/pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),


]
