from django.db.models import Q

# Create your views here.
from decorator.common import CommonDealResponse
from decorator.mydecorator import My_Post
from usermodel.models import User


@My_Post
def register(request):
    try:
        # import time
        # time.sleep(3)
        params = request.POST
        user = User()
        name = params.get('name')
        registeruser = User.objects.filter(name=name)
        # 判断用户是否存在
        if len(registeruser) == 0:
            user.name = name
            user.pwd = params.get('pwd')
            user.is_vip = False
            user.usertype = 3
            user.save()
            mJson = user.toJson()
            return CommonDealResponse.dealResult(True, mJson, "success")
        else:
            return CommonDealResponse.dealResult(False, {}, "账号已存在")
    except Exception as e:
        return CommonDealResponse.dealResult(False, {}, str(e))


@My_Post
def login(request):
    try:
        # import time
        # time.sleep(18)
        params = request.POST
        name = params.get('name')
        registeruser = User.objects.filter(name=name)
        if len(registeruser) == 0:
            return CommonDealResponse.dealResult(False, {}, "该用户尚未注册")
        else:
            pwd = params.get('pwd')
            result = User.objects.filter(Q(name=name) & Q(pwd=pwd))
            # result = User.objects.filter(Q(name=name))
            # result = result.filter(Q(pwd=pwd))
            if len(result) == 0:
                return CommonDealResponse.dealResult(False, {}, "密码不正确")
            else:
                finalResult = result[0]
                return CommonDealResponse.dealResult(True, finalResult.toJson(), "登录成功")
    except Exception as e:
        return CommonDealResponse.dealResult(False, str(e), "failure")
