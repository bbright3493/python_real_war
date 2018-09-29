#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-3 下午12:32
# @Author  : Ztsong
import xadmin

from .models import ProjectShow


xadmin.site.register(ProjectShow)

