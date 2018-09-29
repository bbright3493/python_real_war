#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-8 上午9:49
# @Author  : Ztsong

from django.conf.urls import url

from .views import LivePreviewView, LivePastView

urlpatterns = [
    # 直播预告页
    url(r'^preview/$', LivePreviewView.as_view(), name="live_preview"),
    # 以往直播
    url(r'^past/$', LivePastView.as_view(), name="live_past"),


]