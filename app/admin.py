from django.contrib import admin
from app.models import MenuCategory
from app.models import Greens


# Register your models here.
@admin.register(MenuCategory)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brief', 'category_level', 'category_way', 'parent_category_id', 'add_time')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50



@admin.register(Greens)
class GreensAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brief', 'tips', 'views',
                    'collect', 'makes', 'burden')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 10
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-views',)

    # list_editable 设置默认可编辑字段
    list_editable = ['views', 'collect']

    # fk_fields 设置显示外键字段
    fk_fields = ('category',)

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')

    # 筛选器
    list_filter = ('name', 'views', 'collect', 'category')
    search_fields = ('name','views', 'collect', 'category')

    # Many to many 字段
    filter_horizontal = ('category',)