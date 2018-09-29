# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import ProjectShow
from courses.models import CourseCategory

from operation.models import UserProject
from integral.models import UserIntergral

# Create your views here.

class ProjectShowView(View):
    """
    项目展示
    """
    def get(self, request):
        all_category = CourseCategory.objects.all()

        click_category = request.GET.get("category", "all")
        click_sort = request.GET.get("sort", "new")

        if click_category == "all":
            all_project = ProjectShow.objects.all().order_by("-add_time")
            if click_sort == "hot":
                all_project = all_project.order_by("-click_num")
        else:
            all_project = ProjectShow.objects.filter(coursecategory__category=click_category).order_by("-add_time")
            if click_sort == "hot":
                all_project = all_project.order_by("-click_num")

        # 对项目进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_project, 6, request=request)
        projects = p.page(page)

        return render(request, "project_show.html", {
            "all_category":all_category,
            "click_sort":click_sort,
            "projects":projects,
            "click_category": click_category,
        })


class ProjectResultView(View):
    """
    项目展示结果
    """
    def get(self, request, project_id):

        try:
            project = ProjectShow.objects.get(id=int(project_id))
        except ProjectShow.DoesNotExist:
            project = ProjectShow.objects.all()

        project.click_num += 1
        project.save()

        try:
            user_project = UserProject.objects.get(user=request.user, project=project)
        except:
            user_project = None

        return render(request, "project_result.html", locals())


class JoinPracticeView(View):
    """
    参与项目 用户点击参与项目后的处理
    """
    def post(self, request):

        #判断用户是否已经参与项目
        #扣除所需积分
        #增加用户项目表
        #返回数据

        project_id = request.POST.get("project_id", 1)
        project = ProjectShow.objects.get(id=project_id)

        try:
            user_project = UserProject.objects.get(user=request.user, project=project)
            #该用户已经参与该项目
            value = {"status": "fail1", "msg": "您已经参与该项目"}
            return HttpResponse(json.dumps(value), content_type='application/json')
        except:
            #查询用户积分
            user_intergral = UserIntergral.objects.get(user=request.user)
            if user_intergral.grade - project.integral < 0:
                #用户积分不够的处理
                value = {"status": "fail2", "msg": "您的积分不足"}
                return HttpResponse(json.dumps(value), content_type='application/json')
            else:
                #扣除所需积分
                user_intergral.grade -= project.integral
                user_intergral.save()
                #记录积分 暂时不记录
                #创建用户项目表
                UserProject.objects.create(user=request.user, project=project)
                value = {"status": "success", "msg": "已成功参与项目"}
                return HttpResponse(json.dumps(value), content_type='application/json')

