# _*_ encoding:utf-8 _*_
import datetime
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from utils.alipay import AliPay
from programing.settings import private_key_path, ali_pub_key_path
from .forms import RechargeForm
from .models import OrderInfo, UserIntergral
from operation.models import UserCourse
from users.forms import UserInfoForm
# Create your views here.

class AlipayView(View):

    def get(self, request):
        """
        支付宝返回的return_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091400509243",
            app_notify_url="http://www.zhutaosong.top:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://www.zhutaosong.top:8000/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                try:
                    intergral = UserIntergral.objects.get(user=request.user)
                except:
                    intergral = UserIntergral()
                    intergral.user = request.user
                intergral.grade = int(intergral.grade) + int(existed_order.order_mount * 100)
                intergral.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()

            # user_course = UserCourse.objects.all()
            # obj = UserInfoForm(request.GET, instance=request.user)
            # sign = UserIntergral.objects.get(user=request.user)
            # return render(request, 'user_info.html', {
            #     "user_course": user_course,
            #     "obj": obj,
            #     "sign": sign.grade,
            # })
            return HttpResponseRedirect('/users/info/')


    def post(self, request):
        """
        支付宝返回的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016091400509243",
            app_notify_url="http://www.zhutaosong.top:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://www.zhutaosong.top:8000/alipay/return/"
        )
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                try:
                    intergral = UserIntergral.objects.get(user=request.user)
                except:
                    intergral = UserIntergral()
                    intergral.user = request.user
                print(request.user)
                intergral.grade = int(intergral.grade) + int(existed_order.order_mount * 100)
                intergral.save()
                
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()
                

            return HttpResponse("success")



class RechargeView(View):
    def post(self, request):
        recharge_form = RechargeForm(request.POST)
        if recharge_form.is_valid():
            recharge_money = request.POST.get("recharge", 0)

            print(recharge_money, type(recharge_money))
            alipay = AliPay(
                appid="2016091400509243",
                app_notify_url="http://www.zhutaosong.top:8000/alipay/return/",
                app_private_key_path=private_key_path,
                alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                debug=True,  # 默认False,
                return_url="http://www.zhutaosong.top:8000/alipay/return/"
            )

            # 生成订单号
            now = datetime.datetime.now()
            orderId = now.strftime('%Y%m%d%H%M%S')

            url = alipay.direct_pay(
                subject="[%s]积分充值：%s元"% (request.user, recharge_money),
                out_trade_no=orderId,
                total_amount=int(recharge_money),
            )
            re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
            print(re_url)

            new_order = OrderInfo()
            new_order.user = request.user
            new_order.order_sn = orderId
            new_order.order_mount = float(recharge_money)
            new_order.save()

            value = {"status": "success", "re_url":re_url}
            return HttpResponse(json.dumps(value), content_type="application/json")

        else:
            errors = {"status": "fail", "msg": "输入错误"}
            return HttpResponse(json.dumps(errors), content_type="application/json")