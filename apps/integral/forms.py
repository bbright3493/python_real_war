#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2018/6/3 21:35
# @Author : ZTS
# @Software: PyCharm

from django import forms


class RechargeForm(forms.Form):
    recharge = forms.IntegerField(required=True)
