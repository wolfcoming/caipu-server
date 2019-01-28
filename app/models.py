# -*- coding: utf-8 -*-
import attr as attr
from django.db import models
from datetime import datetime


# Create your models here.
class MenuCategory(models.Model):
    """
    菜单类别
    """
    CATEGORY_LEVEL = (
        (1, "一级类目"),
        (2, "二级类目"),
        (3, "三级类目"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    brief = models.CharField(default="", max_length=200, verbose_name="简短介绍", help_text="简短介绍")  # 简单介绍
    category_level = models.IntegerField(choices=CATEGORY_LEVEL, verbose_name="类目级别", help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, verbose_name="父类别", blank=True,
                                        related_name="sub_cat", on_delete=models.SET_NULL)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "菜单类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Greens(models.Model):
    """
    菜
    """
    name = models.CharField(default="", max_length=20, verbose_name="菜名", help_text="菜名")
    brief = models.CharField(default="", max_length=200, verbose_name="简短介绍", help_text="简短介绍")  # 简单介绍
    tips = models.CharField(default="", max_length=200, verbose_name="小贴士", help_text="小贴士")
    views = models.IntegerField(default=0, verbose_name="浏览量", help_text="浏览量")
    collect = models.IntegerField(default=0, verbose_name="收藏量", help_text="收藏量")
    makes = models.CharField(default="", max_length=1000, verbose_name="步骤", help_text="步骤")
    burden = models.CharField(default="", max_length=1000, verbose_name="用料", help_text="用料")
    category = models.ManyToManyField(to=MenuCategory, verbose_name="类别", help_text="类别")

    class Meta:
        verbose_name = "菜"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def toJSON(self):
        import datetime
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d, ensure_ascii=False)
