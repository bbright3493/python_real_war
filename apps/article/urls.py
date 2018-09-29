#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-5 上午11:51
# @Author  : Ztsong

from django.conf.urls import url

from .views import ArticleListView, ArticleDetailView, ArticleCategoryListView, AddFavView

urlpatterns = [
    #文章列表页
    url(r'^list/$', ArticleListView.as_view(), name="all_article_list"),
    # 文章列表页,按类别列表
    url(r'^(?P<category>\w+)/list/$', ArticleCategoryListView.as_view(), name="article_list"),
    # 文章详情页
  #  url(r'^(?P<category>\w+)/(?P<article_id>\d+)/$', ArticleDetailView.as_view(), name="article_detail"),
    # 文章详情页
    url(r'^(?P<article_id>\d+)/$', ArticleDetailView.as_view(), name="article_detail"),
    #收藏功能
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]

