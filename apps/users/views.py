# _*_ encoding:utf-8 _*_
import json
import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.mixin_utils import LoginRequiredMixin
from article.models import Catagory
from operation.models import UserCourse
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ModifyInfoForm, UserInfoForm, ResetPwdForm
from .models import UserProfile, EmailVerifyRecord, Notice, Banner
from utils.email_send import send_register_email, send_mail_test
from operation.models import *
from integral.models import UserIntergral, IntergralDemand
from article.models import Article
from courses.models import Course
from project.models import ProjectShow


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.

class IndexView(View):
    # 首页
    def get(self, request):
        # 取出轮播图
        # all_banners = Banner.objects.all().order_by('index')
        # courses = Course.objects.filter(is_banner=False)[:6]
        # banner_courses = Course.objects.filter(is_banner=True)[:3]
        # course_orgs = CourseOrg.objects.all()[:15]
        # return render(request, 'index.html', {
        #     'all_banners':all_banners,
        #     'courses':courses,
        #     'banner_courses':banner_courses,
        #     'course_orgs':course_orgs
        # })

        all_banners = Banner.objects.all().order_by('index')

        notice = Notice.objects.first()
        # 新开课程
        new_courses = Course.objects.all().order_by("-add_time")[0:8]

        # 推荐文章
        recommend_posts = Article.objects.filter(is_recommend=True)

        #项目演习
        projects = ProjectShow.objects.all().order_by("-add_time")[0:4]

        # 文章分类
        categories = Catagory.objects.all()
        category_dict = {}
        for category in categories:
            category_dict['%s' % category.name] = '%s' % category.name
        # request.session['category'] = categories
        request.session['category'] = category_dict
#        print(request.session.get('category'))
        for i in request.session.get('category'):
            print(i)
#        print(categories)

        # return render(request, 'index.html', {
        #     "categories": categories,
        #     "recommend_posts": recommend_posts,
        #     "left_new_courses": left_new_courses,
        #     "right_new_course": right_new_course,
        # })
        return render(request, 'index.html', locals())


class ActiveUserView(View):
    """
    激活账户
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:

                # 判断链接的时效性
                send_time = record.send_time
                current_time = datetime.now()
                time_difference = current_time - send_time
                if (time_difference.seconds // 60) <= 60:
                    email = record.email
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                else:
                    email = record.email
                    UserProfile.objects.filter(email=email).delete()
                    return render(request, "active_fail.html")
        else:
            return render(request, "active_fail.html")
        return render(request, "index.html")


class ResetView(View):
    '''邮箱验证后，点击链接修改链接'''

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "resetpwd.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "index.html")


class RegisterView(View):
    """
    注册
    """

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("reusername", "")
            if UserProfile.objects.filter(username=user_name):
                errors = {"status": "fail", "msg": "用户已经注册"}
                return HttpResponse(json.dumps(errors), content_type="application/json")
            pass_wd = request.POST.get("repassword", "")
            nickname = request.POST.get("renickname", "")
            if UserProfile.objects.filter(nick_name=nickname):
                errors = {"status": "fail", "msg": "用户昵称已经被使用"}
                return HttpResponse(json.dumps(errors), content_type="application/json")
            re_emil = request.POST.get("reemail", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = make_password(pass_wd)
            user_profile.nick_name = nickname
            user_profile.email = re_emil
            user_profile.is_active = False
            user_profile.save()

            send_register_email(re_emil, "register")
            value = {"status": "success"}
            return HttpResponse(json.dumps(value), content_type="application/json")
        else:
            errors = {"status": "fail", "msg": "输入错误"}
            return HttpResponse(json.dumps(errors), content_type="application/json")


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    """
    用户登录
    """

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_wd = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_wd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        user_intergral = UserIntergral.objects.get(user=request.user)
                    except UserIntergral.DoesNotExist:
                        user_intergral = UserIntergral()
                        user_intergral.user = request.user
                        user_intergral.grade = 0
                        user_intergral.save()
                    value = {"status": "success"}
                    return HttpResponse(json.dumps(value), content_type="application/json")
                else:
                    errors = {"status": "fail", "msg": "用户没有激活"}
                    return HttpResponse(json.dumps(errors), content_type="application/json")
            else:
                errors = {"status": "fail", "msg": "用户名或密码错误"}
                return HttpResponse(json.dumps(errors), content_type="application/json")
        else:
            errors = {"status": "fail", "msg": "输入错误"}
            return HttpResponse(json.dumps(errors), content_type="application/json")


class ForgetPwdView(View):
    '''忘记密码'''

    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            print(email)
            emailLogin = 'mail.' + email.split('@')[1]
            print(emailLogin)
            value = {"status": "success", "email": email, "emailLogin": emailLogin}
            return HttpResponse(json.dumps(value), content_type="application/json")
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class ResetPwdView(View):
    '''修改用户登陆密码'''

    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "resetpwd.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            value = {"status": "success", "email": email}
            return HttpResponse(json.dumps(value), content_type="application/json")
        else:
            email = request.POST.get("email", "")
            return render(request, "forgetpwd.html", {"email": email, "resetpwd_form": resetpwd_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    个人信息
    """

    def get(self, request):
        user_course = UserCourse.objects.filter(user=request.user)

        user_projects = UserProject.objects.filter(user=request.user)

        obj = UserInfoForm(request.GET, instance=request.user)
        sign = UserIntergral.objects.get(user=request.user)
        return render(request, 'user_info.html', locals())


class UserModifyView(View):
    """
    用户信息修改
    """

    def post(self, request):
        modify_form = ModifyInfoForm(request.POST)
        if modify_form.is_valid():
            modify_nickname = request.POST.get("modify_nickname", "")
            if UserProfile.objects.filter(nick_name=modify_nickname):
                errors = {"status": "fail", "msg": "用户昵称已经被使用"}
                return HttpResponse(json.dumps(errors), content_type="application/json")
            modify_phone = request.POST.get("modify_phone", "")
            modify_email = request.POST.get("modify_email", "")
            modify_address = request.POST.get("modify_address", "")
            modify_about = request.POST.get("modify_about", "")
            user = request.user
            user.nick_name = modify_nickname
            user.mobile = modify_phone
            user.email = modify_email
            user.address = modify_address
            user.sign = modify_about
            user.save()
            value = {"status": "success"}
            return HttpResponse(json.dumps(value), content_type="application/json")
        else:
            errors = {"status": "fail", "msg": "输入错误"}
            return HttpResponse(json.dumps(errors), content_type="application/json")


class ModifyPwdView(View):
    """
    修改密码
    """

    def post(self, request):
        modifyPwd_form = ModifyPwdForm(request.POST)
        if modifyPwd_form.is_valid():
            old_pwd = request.POST.get("old_pwd", "")
            new_pwd = request.POST.get("new_pwd", "")
            confirm_pwd = request.POST.get("confirm_pwd", "")
            if new_pwd != confirm_pwd:
                value = {"status": "fail", "msg": "密码不一致"}
                return HttpResponse(json.dumps(value), content_type='application/json')
            user = request.user
            user.password = make_password(confirm_pwd)
            user.save()
            value = {"status": "success"}
            return HttpResponse(json.dumps(value), content_type="application/json")
        else:
            return HttpResponse(json.dumps(modifyPwd_form.errors), content_type='application/json')


class DateEncoder(json.JSONEncoder):

    def default(self, obj):
        import datetime
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class SignView(View):
    """
    签到
    """

    def post(self, request):
        sign = request.POST.get("sign", "no")
        if sign == "yes":
            request.session['sign'] = sign
        import datetime
        today = datetime.datetime.today()
        # tomorrowemp = today + datetime.timedelta(days=1)
        tomorrowemp = today + datetime.timedelta(minutes=5)
        # tomorrow = tomorrowemp.replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = tomorrowemp.replace()
        interval = tomorrow - datetime.datetime.now()
        sec_interval = interval.days * 24 * 3600 + interval.seconds

        value = {"status": "success", "msg": "已签到"}
        return HttpResponse(json.dumps(value), content_type="application/json")
