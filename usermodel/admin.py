from django.contrib import admin

# Register your models here.
from usermodel.models import UserModel


@admin.register(UserModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'usertype', 'is_vip')