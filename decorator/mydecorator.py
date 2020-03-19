from decorator.common import CommonDealResponse


def My_Post(func):
    def in_fun(request):
        if request.method == 'POST':
            return func(request)
        else:
            return CommonDealResponse.dealResult(False, {}, "只支持post请求")

    return in_fun

def My_Get(func):
    def in_fun(request):
        print("当前请求方法：  "+request.method)
        if request.method == 'GET':
            return func(request)
        else:
            return CommonDealResponse.dealResult(False, {}, "只支持get请求")
    return in_fun