#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-10 上午9:53
# @Author  : Ztsong

from django.conf.urls import url

from .views import UserAdminView, UserAdminSetView

urlpatterns = [
    # 用户信息查询
    url(r'^user_query/$', UserAdminView.as_view(), name="user_query"),
    url(r'^user_set/$', UserAdminSetView.as_view(), name="user_set"),
]
