from django.db import models


class MM94(models.Model):
    """
    94mm数据库表结构
    """
    thumimg = models.CharField(default="", blank=True, null=True, max_length=1000, verbose_name="封面图", help_text="封面图")
    url = models.CharField(default='', max_length=1000, verbose_name="详情地址", help_text="详情地址")
    images = models.CharField(default='', max_length=10000, verbose_name="图片列表", help_text="图片列表")
    title = models.CharField(default='', max_length=200, verbose_name="标题", help_text="标题")

    class Meta:
        verbose_name = '94mm'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name
