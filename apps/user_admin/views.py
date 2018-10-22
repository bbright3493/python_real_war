from django.shortcuts import render
from django.views.generic.base import View

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from users.models import UserProfile
from integral.models import UserIntergral
import json
from courses.models import Course
from operation.models import UserCourse

# Create your views here.


class UserAdminView(View):
    """
    用户后台管理
    """
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'user_admin.html', locals())

    def post(self, request):
        name = request.POST.get("name", 0)
        num = request.POST.get("number", 0)
        course = request.POST.get("course", 0)
        if name:
            try:
                user = UserProfile.objects.get(username=name)
            except:
                print("不存在该用户")
                value = {"status": "fail"}
            else:
                if num:
                    print(num)
                    user_integral = UserIntergral.objects.get(user=user)
                    user_integral.grade += int(num)
                    user_integral.save()
                    value = {"status": "success", "integral": user_integral.grade}
                elif course:
                    print(course)
                    course = Course.objects.get(id=course)
                    #查询是否已经开通该课程
                    try:
                        user_course = UserCourse.objects.get(course=course, user=user)
                    except:
                        user_course = UserCourse.objects.create(user=user, course=course, course_status=2)
                        user_course.save()
                        value = {"status": "success", "info":"成功开通课程"}
                    else:
                        if user_course.cour_status != 2:
                            user_course.cour_status =2
                            user_course.save()
                            value = {"status": "success", "info": "成功开通课程"}
                        else:
                            value = {"status": "fail", "info": "课程已开通"}
                else:
                    print(name)
                    #查询积分和开通课程
                    user_integral = UserIntergral.objects.get(user=user)
                    print(user_integral)
                    value = {"status": "success", "integral": user_integral.grade}
        else:
            value = {"status": "fail"}
        return HttpResponse(json.dumps(value), content_type='application/json')




class UserAdminSetView(View):
    """
    直播预告
    """
    def get(self, request):
        user = request.user
        return render(request, 'user_admin_set.html')

    def post(self, request):
        pass




