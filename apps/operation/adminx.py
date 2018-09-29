#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-10 下午4:06
# @Author  : Ztsong

import xadmin

from .models import UserCourse, UserPass

xadmin.site.register(UserPass)
xadmin.site.register(UserCourse)
