#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-10 下午5:29
# @Author  : Ztsong

from django.conf.urls import url

from .views import *



urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程关卡页
    url(r'^level/(?P<course_id>\d+)/$', CourseLevelView.as_view(), name="course_level"),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/(?P<lesson_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    # 选择题详情页
    url(r'^choice/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<choice_id>\d+)/$', ChoiceQuestionView.as_view(),
        name="choice_question"),

    # 选择题详情页
    url(r'^choice_answer/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<choice_id>\d+)/$', ChoiceQuestionAnswerView.as_view(),
        name="choice_question_answer"),

    # 选择题结果
    url(r'^result/(?P<course_id>\d+)/(?P<lesson_id>\d+)/$', ChoiceResultView.as_view(), name='practice_result'),

    # 在线练习下一题
    url(r'^next/$', NextQuestionView.as_view(), name='next_question'),

    # 编程题详情页
    url(r'^program/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<program_id>\d+)/$', ProgramView.as_view(),
        name="program_question"),

    # 编程详情页
    url(r'^programing/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<program_id>\d+)/$', ProgramingView.as_view(),
        name="programing"),

    # 编程题提交页
    url(r'^program/commit/(?P<course_id>\d+)/(?P<lesson_id>\d+)/(?P<program_id>\d+)/$', ProgramCommitView.as_view(),
        name="program_commit"),

    # 编程题下一题
    url(r'^program_next/$', NextProgramView.as_view(), name='next_program'),

    # 编程题提交页
    url(r'^program/commit/$', ProgramingCommitView.as_view(),name="programing_commit"),

    # 编程题结果
    url(r'^program_result/(?P<course_id>\d+)/(?P<lesson_id>\d+)/$', ProgramResultView.as_view(), name='program_result'),

    # 关卡完成
    url(r'^complete/$', CompleteView.as_view(), name='level_complete'),

    url(r'^downloadurl/$', DownloadUrlView.as_view(), name='download_url'),

    # 编程题上传文件
    url(r'^program/upload/$', ProgramUploadView.as_view(), name='program_upload'),

    url(r'^upload/$', PostView.as_view(), name='post_apply_data'),

]
