# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.utils.timezone import now, timedelta

from .models import LivePreview

# Create your views here.


class LivePreviewView(View):
    """
    直播预告
    """
    def get(self, request):

        live = LivePreview.objects.all().order_by('-add_time').first()

        return render(request, 'live.html', {
            "live": live,
        })


class LivePastView(View):
    """
    以往直播
    """
    def get(self, request):
        print(type(datetime.now))

        print(now())


        past_live = LivePreview.objects.all().order_by('-add_time').exclude(live_time__gt=now())
        print(past_live)

        return render(request, 'live_past.html', {
            "past_live": past_live,
        })
