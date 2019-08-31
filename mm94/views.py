from django.http import HttpResponse


from mm94 import models
from decorator.common import CommonDealResponse


def mmindex(request):
    return HttpResponse(u"欢迎mm")


def getMMList(request):
    datas = models.MM94.objects.all()
    result = []
    for item in datas:
        dic = {}
        dic['url'] = item.url
        dic['images'] = item.images
        dic['title'] = item.title
        dic['thumimg'] = item.thumimg
        result.append(dic)
    return CommonDealResponse.dealResult(True, result, "请求成功")
