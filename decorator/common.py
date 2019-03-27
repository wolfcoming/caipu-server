import json

from django.http import HttpResponse


class CommonDealResponse:
    """
    统一处理返回值
    """
    def dealResult(isSuccess, result, message):
        res = {}
        if isSuccess:
            res['code'] = 1
            res['data'] = result
            res['message'] = message
        else:
            res['code'] = -1
            res['data'] = "失败"
            res['message'] = message
        return HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type='application/json; charset=utf-8')

    def dealNoDateResult():
        res = {}
        res['code'] = 2
        res['data'] = {}
        res['message'] = '暂无数据'
        return HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type='application/json; charset=utf-8')

    def dealNoParamResult(param):
        res = {}
        res['code'] = 3
        res['data'] = []
        res['message'] = param + '  参数找不到'
        return HttpResponse(json.dumps(res, ensure_ascii=False),
                            content_type='application/json; charset=utf-8')