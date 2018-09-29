# -*- coding: utf-8 -*-
"""programing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
import xadmin

from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ResetView, ForgetPwdView
from users.views import ResetPwdView, SignView
from .settings import MEDIA_ROOT
from integral.views import AlipayView, RechargeView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^resetpwd/$', ResetPwdView.as_view(), name="reset_password"),

    # 签到
    url(r'^sign/$', SignView.as_view(), name="sign"),

    url(r'^course/', include('courses.urls', namespace="course")),

    url(r'^article/', include('article.urls', namespace="article")),

    url(r'^live/', include('live.urls', namespace="live")),

    url(r'^users/', include('users.urls', namespace="users")),
    # 项目展示
    url(r'^project/', include('project.urls', namespace="project")),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    # 编程项目文件上传
    # url(r'^upload/$', name='post_apply_data'),

    # 富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

    url(r'^alipay/return/', AlipayView.as_view(), name="alipay"),

    url(r'^recharge/', RechargeView.as_view(), name="recharge"),
]
