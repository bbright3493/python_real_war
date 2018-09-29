#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-3 下午12:32
# @Author  : Ztsong
import xadmin

from .models import UserIntergral, IntegralRecord, OrderInfo, IntergralDemand

xadmin.site.register(UserIntergral)
xadmin.site.register(IntegralRecord)
xadmin.site.register(OrderInfo)
xadmin.site.register(IntergralDemand)
