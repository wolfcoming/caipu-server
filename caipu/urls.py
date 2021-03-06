"""caipu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views as app_views
from usermodel import views as user_views
from mm94 import views as mm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.index),
    path(r'getMenu/', app_views.getMenu),
    path(r'getGreensByid/', app_views.getGreensByid),
    path(r'addMenu/', app_views.addMenu),
    path(r'search/', app_views.search),
    path(r'getBannerData/', app_views.getBannerData),
    path(r'getGreensListByCategory/', app_views.getGreensListByCategory),
    path(r'qntoken/', app_views.qntoken),
    path(r'addCaipu/', app_views.addCaipu),
    path(r'testApi/', app_views.testApi),
    path(r'testApi2/', app_views.testApi2),
    path(r'getTestToken/', app_views.getTestToken),

    path(r'getXmlContentByName/', app_views.getXmlContentByName),
    path(r'getXmlContentByName2/', app_views.getXmlContentByName2),

    # 用户模块
    path(r'register/', user_views.register),
    path(r'login/', user_views.login),
    path(r'websocketTest/', user_views.websocketTest),

    # 94mm接口
    path(r'mm/', mm.mmindex),
    path(r'getMmList/', mm.getMMList),

    # 测试接口
    path(r'testPost/', app_views.testPost)

]
