import uuid
from uuid import UUID

from django.db import models


# Create your models here.


class User(models.Model):
    """
    用户模型
    """
    USERTYPE = (
        (1, "QQ"),
        (2, "WX"),
        (3, "ZC")
        # 注册用户
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, verbose_name="用户id", help_text="用户id")
    name = models.CharField(default="", max_length=30, verbose_name="用户名", help_text="用户名")
    pwd = models.CharField(default="", max_length=120, verbose_name="密码", help_text="密码")
    headimg = models.CharField(default="", max_length=100, null=True, blank=True, verbose_name="用户头像", help_text="用户头像")
    usertype = models.IntegerField(default=3, verbose_name="登录类型", help_text="登录类型")
    is_vip = models.BooleanField(default=False, null=True, blank=True, verbose_name="是否是vip", help_text="vip用户")
    brief = models.CharField(default="暂无简介", max_length=200, null=True, blank=True, verbose_name="个人简介",
                             help_text="个人简介")

    class Meta:
        verbose_name = "用户模型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def toJson(self):
        result = {}
        result['id'] = str(self.id)
        result['name'] = self.name
        result['pwd'] = self.pwd
        result['heading'] = self.headimg
        result['usertype'] = self.usertype
        result['is_vip'] = self.is_vip
        result['brief'] = self.brief
        return result
