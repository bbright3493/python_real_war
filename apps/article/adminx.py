#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-5 上午11:51
# @Author  : Ztsong

import xadmin

from .models import Tag, Article, Catagory


class ArticleAdmin(object):
    style_fields = {"content":"ueditor"}

xadmin.site.register(Tag)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Catagory)

