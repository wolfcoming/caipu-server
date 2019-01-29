# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app import models
from django.core import serializers
import json
import datetime
from django.db.models import Count


# Create your views here.
def index(request):
    return HttpResponse(u"欢迎")


def getMenu(request):
    """
    获取菜单列表
    :param request:
    :return:
    """
    try:
        menu_list = models.MenuCategory.objects.values('id', 'name', 'category_level', 'parent_category')
        menu_list_json = json.dumps(list(menu_list), ensure_ascii=False, cls=DateEncoder)
        print(menu_list_json)
        return CommonDealResponse.dealResult(True, json.loads(menu_list_json), "成功")

        # menu_list = models.MenuCategory.objects.all()
        # menu_list_json = serializers.serialize("json", menu_list, ensure_ascii=False)
        # print(menu_list_json)
        # return HttpResponse(menu_list_json, content_type='application/json; charset=utf-8')

    except Exception as e:
        return CommonDealResponse.dealResult(False, {}, e)


def getGreensList(request):
    """
    获取菜列表
    :return:
    """
    try:

        # greens_list = models.Greens.objects.values()  # 使用values 没有category字段 使用all有
        # greens_list = json.dumps(list(greens_list), ensure_ascii=False)
        # return HttpResponse(greens_list, content_type='application/json; charset=utf-8')

        # 手动解析数据
        # defer 过滤某些不需要的字段
        # prefetch_related 是优化关联查询
        # prefetch_related是通过再执行一条额外的SQL语句，然后用 Python 把两次SQL查询的内容关联（joining)到一起
        templist = models.Greens.objects.defer("brief", "tips", "makes").prefetch_related('category').all()
        result = []
        for tem in templist:
            dic = {}
            dic['name'] = tem.name
            dic['id'] = tem.id
            dic['views'] = tem.views
            dic['collect'] = tem.collect

            # 调用改方法会再次执行数据库查询 若不需要 就别查询  如果使用 可以使用prefetch_related 进行优化
            category = []
            for categoryItem in tem.category.all():
                category.append(categoryItem.id)
            dic['category'] = category

            result.append(dic)
        return CommonDealResponse.dealResult(True, result, "请求成功")
    except:
        CommonDealResponse.dealResult(False, {}, "请求失败")


def getGreensByid(request):
    """
    获取菜详情
    :param request:
    :return:
    """
    id = request.GET.get("id")
    greens = models.Greens.objects.get(id=id)
    if greens:
        greensJson = json.loads(greens.toJSON())
        # 获取该菜的所属的类别
        category = []
        for categoryItem in greens.category.all():
            category.append(categoryItem.id)
        greensJson['category'] = category
        return CommonDealResponse.dealResult(True, greensJson, "成功")
    else:
        return CommonDealResponse.dealNoDateResult()


class DateEncoder(json.JSONEncoder):
    """
    解决json解析时间问题
    """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONDecoder.default(self, o)


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
            res['data'] = {}
            res['message'] = message
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json; charset=utf-8')

    def dealNoDateResult():
        res = {}
        res['code'] = 2
        res['data'] = {}
        res['message'] = '暂无数据'
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type='application/json; charset=utf-8')
