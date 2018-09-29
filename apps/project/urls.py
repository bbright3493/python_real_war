#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-21 上午10:45
# @Author  : Ztsong

from django.conf.urls import url

from .views import ProjectShowView, ProjectResultView, JoinPracticeView

urlpatterns = [
    # 文章列表页
    url(r'^list/', ProjectShowView.as_view(), name="project_list"),

    url(r'^join/', JoinPracticeView.as_view(), name="join_project"),

    url(r'^(?P<project_id>\d+)/$', ProjectResultView.as_view(), name="project_result"),

]
