# coding:utf-8
from django.http import HttpResponse
from app import models
import json
import datetime
from django.core.paginator import Paginator, EmptyPage
import qiniu

from caipu.settings import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME
from decorator.common import CommonDealResponse
from decorator.mydecorator import My_Get, My_Post
from usermodel.models import User


@My_Get
def qntoken(request):
    """
    获取七牛token
    :param request:
    :return:
    """
    access_key = QINIU_ACCESS_KEY
    secret_key = QINIU_SECRET_KEY
    q = qiniu.Auth(access_key, secret_key)

    bucket = QINIU_BUCKET_NAME  # 七牛云的存储空间名
    token = q.upload_token(bucket)
    return CommonDealResponse.dealResult(True, token, "获取成功")


def index(request):
    return HttpResponse(u"欢迎")


@My_Post
def addCaipu(request):
    try:
        # import time
        # time.sleep(5)
        body = json.loads(request.body)
        greens = models.Greens()
        greens.name = body['name']
        greens.brief = body['brief']
        greens.tips = body['tips']
        greens.views = body['views']
        greens.collect = body['collect']
        greens.makes = body['makes']
        greens.burden = body['burden']
        greens.img = body['img']

        userid = body['userid']
        user = User.objects.get(id=userid)
        if (user != None):
            greens.user = user

        greens.save()
        return CommonDealResponse.dealResult(True, "请求成功", "success")
    except Exception as e:
        return CommonDealResponse.dealResult(False, str(e), "fail")


def addMenu(request):
    """
    添加菜单 ：测试使用
    :param request:
    :return:
    """
    parent_category = models.MenuCategory.objects.get(id=1)
    result = models.MenuCategory(name="凉菜", brief="凉菜",
                                 category_level=2, category_way=1,
                                 parent_category=parent_category).save()
    print(result)
    return HttpResponse(result)


@My_Get
def getMenu(request):
    """
    获取菜单列表
    :param request:
    :return:
    """
    try:
        # import time
        # time.sleep(6)
        category_way = request.GET.get('category_way')
        menu_list = []
        if category_way:
            menu_list = models.MenuCategory.objects.filter(category_way=category_way).values('id', 'name',
                                                                                             'category_level',
                                                                                             'parent_category',
                                                                                             'imgurl')
        else:
            menu_list = models.MenuCategory.objects.values('id', 'name', 'category_level', 'parent_category', 'imgurl')
        menu_list_json = json.dumps(list(menu_list), ensure_ascii=False, cls=DateEncoder)
        print(menu_list_json)
        return CommonDealResponse.dealResult(True, json.loads(menu_list_json), "成功")

        # menu_list = models.MenuCategory.objects.all()
        # menu_list_json = serializers.serialize("json", menu_list, ensure_ascii=False)
        # print(menu_list_json)
        # return HttpResponse(menu_list_json, content_type='application/json; charset=utf-8')

    except Exception as e:
        return CommonDealResponse.dealResult(False, {}, e)


@My_Get
def getGreensListByCategory(request):
    """
    获取菜单下的所有菜品 (废弃，不要硬关联）
    :param request:
    :return:
    """
    categoryId = request.GET.get("categoryid")
    pageSize = request.GET.get("pageSize")
    pageNumber = request.GET.get("pageNumber")
    if pageSize == None or pageNumber == None or categoryId == None:
        return CommonDealResponse.dealNoParamResult("categoryId or pageSize or pageNumber")

    category = models.MenuCategory.objects.get(id=categoryId)
    list = models.Greens.objects.filter(category=category).order_by('views')
    try:
        paginator = Paginator(list, pageSize)
        list = paginator.page(pageNumber).object_list
    except EmptyPage:
        return CommonDealResponse.dealResult(True, [], "无数据")
    result = []
    for item in list:
        dic = {}
        dic['id'] = item.id
        dic['name'] = item.name
        dic['img'] = item.img
        result.append(dic)
    return CommonDealResponse.dealResult(True, result, "请求成功")


def search(request):
    """
    搜索菜
    :param request:
    :return:
    """
    try:
        # import time
        # time.sleep(3)
        pageSize = request.GET.get("pageSize")
        pageNumber = request.GET.get("pageNumber")
        name = request.GET.get("name")

        if pageSize == None or pageNumber == None or name == None:
            return CommonDealResponse.dealNoParamResult("参数缺失")
        else:
            templist = models.Greens.objects.defer("brief", "tips", "makes") \
                .filter(name__contains=name).all() \
                # .order_by( '-views')
            paginator = Paginator(templist, pageSize)
            try:
                templist = paginator.page(pageNumber).object_list
            except EmptyPage:
                return CommonDealResponse.dealResult(True, [], "无数据")
            result = []
            for tem in templist:
                dic = {}
                dic['name'] = tem.name
                dic['id'] = tem.id
                dic['views'] = tem.views
                dic['collect'] = tem.collect
                dic['burden'] = tem.burden
                dic['img'] = tem.img
                # 调用改方法会再次执行数据库查询 若不需要 就别查询  如果使用 可以使用prefetch_related 进行优化
                category = []
                for categoryItem in tem.category.all():
                    category.append(categoryItem.id)
                dic['category'] = category

                result.append(dic)
            return CommonDealResponse.dealResult(True, result, "请求成功")
    except Exception:
        return CommonDealResponse.dealResult(False, {}, "请求失败")


@My_Get
def getGreensByid(request):
    """
    获取菜详情
    :param request:
    :return:
    """
    try:
        params = ""
        if request.method == "GET":
            params = request.GET
        else:
            params = request.POST

        id = params.get("id")
        if id == None:
            return CommonDealResponse.dealNoParamResult('id')
        greens = models.Greens.objects.filter(id=id).first()

        # 更新浏览量
        views = greens.views
        views += 1
        greens.views = views
        greens.save()

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
    except Exception as e:
        return CommonDealResponse.dealResult(False, {}, "fail")


def getBannerData(request):
    lists = models.Banner.objects.all()
    result = []
    for item in lists:
        dic = {}
        dic['name'] = item.category.name
        dic['img'] = item.img
        dic['category_id'] = item.category.id
        result.append(dic)
    return CommonDealResponse.dealResult(True, result, "请求成功")


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

# 北京银行测试
def getXmlContentByName(request):
    """
    根据文件名 来读取文件内容，方便客户端调试代码
    :param request:
    :return:
    """
    try:
        filePath = "/Users/yangqing/Develop/android/projects/bjyh/normal/bjyh2_Q/eMPView/src/main/assets/test/"
        params = ""
        if request.method == "GET":
            params = request.GET
        else:
            params = request.POST
        name = params.get("name")
        if name == None:
            return HttpResponse("name is none")
        f = open(filePath + name + ".xml")
        content = f.read()
        return HttpResponse(content)
    except Exception as e:
        return HttpResponse("can not open file")

# 北京银行测试
def getXmlContentByName2(request):
    """
    根据文件名 来读取文件内容，方便客户端调试代码
    :param request:
    :return:
    """
    try:
        filePath = "/Users/yangqing/Develop/android/projects/bjyh/zhengshi/new_android_studio/eMPView/src/main/assets/test/"
        params = ""
        suffix = ""
        if request.method == "GET":
            params = request.GET
        else:
            params = request.POST
        name = params.get("name")
        if name == None:
            return HttpResponse("name is none")
        if ".html" in name:
            suffix = ".html"
        else:
            suffix = ".xml"
        f = open(filePath + name + suffix)
        content = f.read()
        return HttpResponse(content)
    except Exception as e:
        return HttpResponse("can not open file")
