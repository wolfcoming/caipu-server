from django.contrib import admin

# Register your models here.
from usermodel.models import User


@admin.register(User)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'usertype', 'is_vip')
