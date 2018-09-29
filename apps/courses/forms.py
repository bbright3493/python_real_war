#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-7 上午10:05
# @Author  : Ztsong

from django import forms

from .models import ProgramUpload

#
# class ProgramUploadForm(forms.ModelForm):
#     class Meta:
#         model = ProgramUpload
#         fields = ['image']


class ProgramUploadForm(forms.Form):
    image = forms.ImageField()



