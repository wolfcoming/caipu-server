from decorator.common import CommonDealResponse


def My_Post(func):
    def in_fun(request):
        if request.method == 'POST':
            return func(request)
        else:
            return CommonDealResponse.dealResult(False, "只支持post请求", "失败")

    return in_fun

def My_Get(func):
    def in_fun(request):
        if request.method == 'GET':
            return func(request)
        else:
            return CommonDealResponse.dealResult(False, "只支持post请求", "失败")

    return in_fun