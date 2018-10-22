# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from .models import Course, Lesson, ChoiceQuestion, Video, ProgramQuestion, ChoiceBank, ProgramUpload, CourseCategory, \
    Faq
from .models import CourseDirection, KnowledgePoint
from article.models import Article
from operation.models import UserCourse, UserPass, UserErrorChoice
from integral.models import UserIntergral, IntergralDemand
from .forms import ProgramUploadForm
from project.models import ProjectShow

# Create your views here.


class CourseListView(View):
    """
    课程列表页
    """

    def get(self, request):
        all_category = CourseCategory.objects.all()
        all_direction = CourseDirection.objects.all()
        click_direction = request.GET.get("direction", "all")
        click_category = request.GET.get("category", "all")
        click_degree = request.GET.get("degree", "all")
        click_sort = request.GET.get("sort", "new")
        print(click_direction)

        if click_direction == "all":
            if click_category == "all":
                if click_degree == "all":
                    all_course = Course.objects.all().order_by("-add_time")
                    if click_sort == "hot":
                        all_course = Course.objects.all().order_by("-students")
                else:
                    all_course = Course.objects.filter(degree=click_degree).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
            else:
                if click_degree == "all":
                    all_course = Course.objects.filter(coursecategory__category=click_category).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
                else:
                    all_course = Course.objects.filter(coursecategory__category=click_category,
                                                       degree=click_category).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
        else:
            all_course = Course.objects.filter(direction=click_direction)
            print("all:", all_course)
            if click_category == "all":
                if click_degree == "all":
                    all_course = all_course.order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
                else:
                    all_course = all_course.filter(degree=click_degree).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
            else:
                if click_degree == "all":
                    all_course = all_course.filter(coursecategory__category=click_category).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
                else:
                    all_course = all_course.filter(coursecategory__category=click_category,
                                                   degree=click_category).order_by("-add_time")
                    if click_sort == "hot":
                        all_course = all_course.order_by("-students")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 6, request=request)

        courses = p.page(page)
        print(type(courses))

        print("session:", request.session.get('Linux', default="Html"))

        return render(request, 'course_list.html', {
            "all_direction": all_direction,
            "all_course": courses,
            "all_category": all_category,
            "click_direction": click_direction,
            "click_category": click_category,
            "click_degree": click_degree,
            "click_sort": click_sort,
        })


class CourseLevelView(View):
    """
    课程关卡列表页
    显示关卡时同时查询用户关卡信息 需要显示用户对应关卡对学习情况
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程

        try:
            user_course = UserCourse.objects.get(user=request.user, course=course)
        except:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        students = UserCourse.objects.all().count()
        course.students = int(students)
        course.save()

        all_level = Lesson.objects.filter(course=course_id).order_by("add_time")
        this_level = Lesson.objects.filter(course=course_id).first()
        # 对该课程对所有关卡 查询对应对用户关卡表 如果没有 则新建
        for level in all_level:
            try:
                cur_user_level = UserPass.objects.get(user=request.user, lesson=level)
            except:
                cur_user_level = UserPass(user=request.user, lesson=level)
                cur_user_level.save()

        user_levels = UserPass.objects.filter(user=request.user, lesson__course=course).order_by("lesson")

        # # 下一关关卡
        # try:
        #     next_level = Lesson.objects.filter(course=course_id).order_by("add_time")[Level_num+1]
        # except IndexError:
        #     next_level = Lesson.objects.filter(course=course_id).order_by("add_time")[Level_num]
        #
        # # 开通下一关关卡
        # if this_level.pass_level:
        #     next_level.pass_level = True

        last_level = Lesson.objects.filter(course=course_id).last()

        projects = ProjectShow.objects.filter(course=course)

        return render(request, 'course_level.html', locals())


class CourseDetailView(View):
    """
    关卡详情页
    """

    def get(self, request, course_id, lesson_id):
        course = Course.objects.get(id=course_id)

        # 查询用户课程状态 如果是未学习 则将状态改为正在学习
        user_course = UserCourse.objects.get(user=request.user, course=course)
        if user_course.study_status == 1:
            user_course.study_status = 2
            user_course.save()

        lesson = Lesson.objects.get(id=lesson_id)
        try:
            user_lesson = UserPass.objects.get(user=request.user, lesson=lesson)
        except:
            user_lesson = UserPass(user=request.user, lesson=lesson)
            user_lesson.save()

        print(lesson)

        # user_intergral = UserIntergral.objects.get(user=request.user)
        extend_demand = IntergralDemand.objects.get(lesson_id=int(lesson_id), demand='extend_download')
        # explain_demand = IntergralDemand.objects.get(lesson_id=int(lesson_id), demand='pro_explain')

        all_vedio = Video.objects.filter(lesson_id=lesson_id)
        all_article = Article.objects.filter(lesson=lesson).order_by('no')
        choice_bank = lesson.get_choice_bank()
        program_bank = lesson.get_program_bank()
        faqs = Faq.objects.filter(lesson=lesson)
        knowledge_points = KnowledgePoint.objects.filter(lesson=lesson)
        lesson_projects = ProjectShow.objects.filter(lesson=lesson)
        return render(request, 'course_detail.html', locals())


class ChoiceQuestionAnswerView(View):
    """
    选择题题目
    """

    def get(self, request, course_id, lesson_id, choice_id):
        lesson_choices = ChoiceQuestion.objects.filter(lesson_id=int(lesson_id))
        this_question = ChoiceQuestion.objects.get(id=choice_id)
        all_question_num = ChoiceQuestion.objects.filter(lesson_id=int(lesson_id)).count()

        is_last = False
        if int(choice_id) == all_question_num:
            is_last = True

        return render(request, 'choice_answer.html', locals())


class ChoiceQuestionView(View):
    """
    选择题题目
    """

    def get(self, request, course_id, lesson_id, choice_id):
        lesson_choices = ChoiceQuestion.objects.filter(lesson_id=int(lesson_id))
        this_question = ChoiceQuestion.objects.get(id=choice_id)
        all_question_num = ChoiceQuestion.objects.filter(lesson_id=int(lesson_id)).count()
        print(all_question_num)

        if int(this_question.question_num) == 1:
            request.session['right_count'] = 0
            request.session['error'] = []

        is_last = False
        if this_question.question_num == all_question_num:
            is_last = True
            next_question = this_question
        else:
            next_question = ChoiceQuestion.objects.get(question_num=this_question.question_num+1,
                                                       choicebank=this_question.choicebank)

        return render(request, 'choice_pra.html', locals())


class NextQuestionView(View):
    """
    下一题
    """

    def post(self, request):
        this_question = request.POST.get("practice_num", 1)
        user_answer = request.POST.get("user_answer", "")

        if int(user_answer) != -1:
            # 得到本题的正确答案
            right = ChoiceQuestion.objects.get(id=int(this_question))
            right_answer = right.answer
            if int(user_answer) + 1 == right_answer:
                print("答对本题")
                request.session['right_count'] = request.session.get('right_count', default=0) + 1
            else:
                print("本题错误")
                l = request.session['error']
                l.append(right.id)
                request.session['error'] = l

                user_pass = UserPass.objects.get(user=request.user, lesson=right.lesson)

                # 判断是否第一次提交答案
                if user_pass.choice_status == 0:
                    user_course = UserCourse.objects.get(user=request.user, course=right.lesson.course)
                    # 判断是否开通课程vip或者关卡vip
                    if user_course.course_status == 2 or user_pass.status == 2:
                        error_question = UserErrorChoice()
                        error_question.user = request.user
                        error_question.choice = right
                        error_question.user_answer = int(user_answer) + 1
                        error_question.save()

            value = {"status": "success"}
            print("session", request.session['right_count'])
            return HttpResponse(json.dumps(value), content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"没有进行选择"}', content_type='application/json')


class ChoiceResultView(View):
    """
    选择题结果
    """

    def get(self, request, course_id, lesson_id):
        right_nums = request.session.get('right_count', default=0)
        user_errors = request.session.get('error', default=[])
        errors = []
        for error in user_errors:
            errors.append(ChoiceQuestion.objects.get(id=int(error)))

        print("right_nums:", right_nums)
        all_question_num = ChoiceQuestion.objects.filter(lesson_id=int(lesson_id)).count()
        print("all_num:", all_question_num)
        right_rate = int(int(right_nums) / float(all_question_num) * 100)
        print(right_rate)
        lesson = Lesson.objects.get(id=lesson_id)
        course = Course.objects.get(id=course_id)

        # 保存提交状态 只有开通了vip的用户才修改该状态
        user_pass = UserPass.objects.get(user=request.user, lesson=lesson)
        user_course = UserCourse.objects.get(user=request.user, course=course)
        if user_pass.choice_status == 0 and (user_pass.status == 2 or user_course.course_status == 2):
            user_pass.choice_status = 1
            user_pass.save()

        return render(request, 'choice_result.html', locals())


class ProgramView(View):
    """
    编程题
    """

    def get(self, request, course_id, lesson_id, program_id):
        # program_file = ProgramQuestion.objects.get(course=int(course_id), lesson=int(lesson_id), id=int(program_id))
        program = ProgramQuestion.objects.get(id=program_id)

        all_question_num = ProgramQuestion.objects.filter(program_bank=program.program_bank).count()

        if int(program.question_num) == 1:
            request.session['right_count_program'] = 0
            request.session['error_program'] = []

        is_last = False
        #判断是否最后一题
        if program.question_num == all_question_num:
            is_last = True
            next_program = program
        else:
            next_program = ProgramQuestion.objects.get(question_num=program.question_num+1, program_bank=program.program_bank )
        try:
            program_result = ProgramUpload.objects.get(programquestion_id=int(program_id), user=request.user)
        except ProgramUpload.DoesNotExist:
            program_result = ProgramUpload.objects.all()
        print(program_result)

        return render(request, 'program.html', locals())


class ProgramingView(View):
    """
    编程题的编程页面
    """

    def get(self, request, course_id, lesson_id, program_id):
        # program_file = ProgramQuestion.objects.get(course=int(course_id), lesson=int(lesson_id), id=int(program_id))
        program = ProgramQuestion.objects.get(id=program_id)
        try:
            program_result = ProgramUpload.objects.get(programquestion_id=int(program_id), user=request.user)
        except ProgramUpload.DoesNotExist:
            program_result = ProgramUpload.objects.all()
        print(program_result)

        return render(request, 'program_start.html', locals())


class ProgramingCommitView(View):
    """
    代码提交的处理
    """

    def post(self, request):
        user_answer = request.POST.get("code", "")

        program_id = request.POST.get("program_id", "")

        print(user_answer)

        program_question = ProgramQuestion.objects.get(id=int(program_id))

        if program_question.result == user_answer:
            value = {"status": "success", "result": "ok"}
        else:
            value = {"status": "success", "result": "error"}

        return HttpResponse(json.dumps(value), content_type='application/json')


class NextProgramView(View):
    """
    下一题
    """

    def post(self, request):
        this_question_num = request.POST.get("practice_num", 1)
        this_question_id = request.POST.get("practice_id", 1)
        result = request.POST.get("result", "")

        this_program = ProgramQuestion.objects.get(id=this_question_id)

        if int(result) == 1:
            print("答对本题")

            request.session['right_count_program'] = request.session.get('right_count_program', default=0) + 1

        else:
            print("本题错误")
            l = request.session['error_program']
            l.append(this_program.id)
            request.session['error_program'] = l

        value = {"status": "success"}
        print("session", request.session['right_count_program'])
        return HttpResponse(json.dumps(value), content_type='application/json')


class ProgramCommitView(View):
    """
    编程题
    """

    def get(self, request, course_id, lesson_id, program_id):
        # program_file = ProgramQuestion.objects.get(course=int(course_id), lesson=int(lesson_id), id=int(program_id))

        try:
            program_result = ProgramUpload.objects.get(programquestion_id=int(program_id), user=request.user)
        except ProgramUpload.DoesNotExist:
            program_result = ProgramUpload.objects.all()
        print(program_result)

        return render(request, 'program-commit.html', {
            # "program_file": program_file,
            "program_result": program_result,
            "program_id": program_id,
        })


class ProgramUploadView(View):
    """
    编程项目上传
    """

    def post(self, request):
        file_obj = request.FILES.get('file')
        image_obj = request.FILES.get('image')
        learned_obj = request.POST.get('learn')
        programId_obj = request.POST.get('programId')
        program = ProgramQuestion.objects.get(id=int(programId_obj))
        # user = request.user
        if file_obj and image_obj:
            program_result = ProgramUpload()
            program_result.programquestion = program
            program_result.user = request.user
            program_result.upload = file_obj
            program_result.image = image_obj
            program_result.learned = learned_obj
            program_result.is_complete = True
            program_result.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ProgramResultView(View):
    """
    编程题结果
    """
    def get(self, request, course_id, lesson_id):
        right_nums = request.session.get('right_count_program', default=0)
        user_errors = request.session.get('error_program', default=[])
        errors = []
        for error in user_errors:
            errors.append(ProgramQuestion.objects.get(id=int(error)))

        errors = list(set(errors))

        print("right_nums:", right_nums)
        all_question_num = ProgramQuestion.objects.filter(lesson_id=int(lesson_id)).count()
        print("all_num:", all_question_num)
        right_rate = int(int(right_nums) / float(all_question_num) * 100)
        print(right_rate)
        lesson = Lesson.objects.get(id=lesson_id)
        course = Course.objects.get(id=course_id)

        return render(request, 'program_result.html', locals())


class PostView(View):
    def post(self, request):
        import time
        import os
        from programing import settings
        file_obj = request.FILES.get('file')
        image_obj = request.FILES.get('image')
        if file_obj:  # 处理附件上传到方法
            request_set = {}
            print('file--obj', file_obj)
            # user_home_dir = "upload/%s" % (request.user.userprofile.id)
            accessory_dir = settings.BASE_DIR
            if not os.path.isdir(accessory_dir):
                os.mkdir(accessory_dir)
            upload_file = "%s/%s" % (accessory_dir, file_obj.name)
            recv_size = 0
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
            order_id = time.strftime("%Y%m%d%H%M%S", time.localtime())
            # cache.set(order_id, upload_file)
            return HttpResponse(order_id)


class CompleteView(View):
    """
    关卡完成
    """

    def post(self, request):
        course_id = request.POST.get("course_id", 1)
        lesson_id = request.POST.get("lesson_id", 1)
        print(type(int(course_id)), int(course_id))
        this_lesson = Lesson.objects.get(course_id=int(course_id), id=int(lesson_id))
        print(this_lesson)
        this_lesson.pass_level = True
        last_level = Lesson.objects.filter(course=int(course_id)).last()
        print(last_level)

        choice_bank = ChoiceBank.objects.get(lesson=int(lesson_id))
        print(choice_bank)
        program_question = ProgramQuestion.objects.get(lesson=int(lesson_id))

        if choice_bank.is_complete == True and program_question.is_complete == True:
            if int(lesson_id) != last_level.id:
                next_level = Lesson.objects.filter(course=int(course_id)).order_by("-add_time")[int(lesson_id) + 1]
                print("next:", next_level)
                next_level.open_level = True
                this_lesson.pass_level = True
                this_lesson.save()
                next_level.save()
            else:
                this_lesson.pass_level = True
                this_lesson.save()

            value = {"status": "success", "msg": "已完成"}
            return HttpResponse(json.dumps(value), content_type='application/json')
        else:
            value = {"status": "fail", "msg": "你还没有完成全部任务"}
            return HttpResponse(json.dumps(value), content_type='application/json')


# class ProjectShowView(View):
#     """
#     项目展示
#     """
#
#     def get(self, request):
#         all_category = CourseCategory.objects.all()
#
#         click_category = request.GET.get("category", "all")
#         click_course = request.GET.get("course", "all")
#         click_level = request.GET.get("level", "all")
#         all_level = Lesson.objects.filter(course__name=click_course)
#
#         if click_category == "all":
#             print("category:", click_category)
#             all_project = ProgramUpload.objects.filter(is_show=True).order_by("-add_time")
#             all_course = Course.objects.filter()
#         else:
#             all_course = Course.objects.filter(coursecategory__category=click_category)
#             if click_course == "all":
#
#                 all_project = ProgramUpload.objects.filter(lesson__course__coursecategory__category=click_category,
#                                                            is_show=True)
#             else:
#                 if click_level == "all":
#
#                     all_project = ProgramUpload.objects.filter(lesson__course__coursecategory__category=click_category,
#                                                                lesson__course__name=click_course,
#                                                                is_show=True)
#                 else:
#
#                     all_project = ProgramUpload.objects.filter(lesson__course__coursecategory__category=click_category,
#                                                                lesson__course__name=click_course,
#                                                                lesson__name=click_level,
#                                                                is_show=True)
#         # 对课程进行分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#
#         p = Paginator(all_project, 6, request=request)
#         projects = p.page(page)
#
#         return render(request, "project_show.html", {
#             "all_category": all_category,
#             "click_category": click_category,
#             "all_course": all_course,
#             "click_course": click_course,
#             "all_level": all_level,
#             "click_level": click_level,
#             "projects": projects,
#
#         })


# class ProjectResultView(View):
#     """
#     项目展示结果
#     """
#
#     def get(self, request, lesson):
#         try:
#             program_result = ProgramUpload.objects.get(lesson__name=lesson, user=request.user)
#         except ProgramUpload.DoesNotExist:
#             program_result = ProgramUpload.objects.all()
#         print(program_result)
#         return render(request, "project_result.html", {
#             "program_result": program_result
#         })


class DownloadUrlView(View):
    """链接下载"""

    def post(self, request):
        course_id = request.POST.get("course_id", 1)
        lesson_id = request.POST.get("lesson_id", 1)
        type = request.POST.get("type", "")
        user_intergral = UserIntergral.objects.get(user=request.user)
        demand_intergral = IntergralDemand.objects.get(lesson_id=int(lesson_id), demand=type)
        if user_intergral.grade >= demand_intergral.intergral:
            user_intergral.grade = user_intergral.grade - demand_intergral.intergral
            user_intergral.save()
            demand_intergral.download_count += 1
            demand_intergral.save()
            value = {"status": "success", "re_url": demand_intergral.url}
            return HttpResponse(json.dumps(value), content_type='application/json')
        else:
            value = {"status": "fail", "msg": "您的积分不足，请充值!"}
            return HttpResponse(json.dumps(value), content_type='application/json')
