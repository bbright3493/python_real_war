#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-3 下午12:32
# @Author  : Ztsong
import xadmin

from .models import Course, ChoiceQuestion, Video, Lesson, Faq, ChoiceBank, ProgramQuestion, ProgramUpload
from .models import CourseCategory, CourseDirection, ProgramBank

# xadmin.site.register(CourseDirection)
xadmin.site.register(CourseCategory)
xadmin.site.register(Course)
xadmin.site.register(Lesson)
xadmin.site.register(Video)
xadmin.site.register(ChoiceBank)
xadmin.site.register(ChoiceQuestion)
xadmin.site.register(ProgramQuestion)
xadmin.site.register(ProgramBank)
xadmin.site.register(ProgramUpload)
xadmin.site.register(Faq)
