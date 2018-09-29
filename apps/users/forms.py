# -*- coding: utf-8 -*-
__author__ = 'bb'
__date__ = '2018/3/25'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
from operation.models import UserQuestionTeacher
from DjangoUeditor.forms import UEditorModelForm


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class ModifyInfoForm(forms.Form):
    nick_name = forms.CharField(required=False)
    mobile = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(required=False)
    sign = forms.CharField(required=False)


# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'password']


class RegisterForm(forms.Form):
    reusername = forms.CharField(required=True)
    repassword = forms.CharField(required=True, min_length=5)
    renickname = forms.CharField(required=True)
    reemail = forms.EmailField(required=True)
    # captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
    email = forms.EmailField(required=True)


class ModifyPwdForm(forms.Form):
    old_pwd = forms.CharField(required=True, min_length=5)
    new_pwd = forms.CharField(required=True, min_length=5)
    confirm_pwd = forms.EmailField(required=True)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'mobile', 'email', 'sign', 'address']


class UserQuestionTeacherForm(UEditorModelForm):
    class Meta:
        model = UserQuestionTeacher
        fields = ['question_content']
