#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-8 上午9:49
# @Author  : Ztsong

import xadmin

from .models import LivePreview


class LivePreviewAdmin(object):
    style_fields = {"content":"ueditor"}

xadmin.site.register(LivePreview, LivePreviewAdmin)

