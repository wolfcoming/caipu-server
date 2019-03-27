from django.shortcuts import render

# Create your views here.
from decorator.common import CommonDealResponse
from usermodel.models import User


def register(request):
    try:
        user = User()
        user.name = "测试用户"
        user.headimg = "111122"
        user.is_vip = False
        user.usertype = 3
        user.save()
        return CommonDealResponse.dealResult(True, "注册成功", "success")
    except Exception as e:
        return CommonDealResponse.dealResult(False, str(e), "failure")
