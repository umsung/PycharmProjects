from django.contrib import admin
from personal_blog.models import *
# Register your models here.

# admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Post)
admin.site.register(Comment)

admin.site.site_title = '博客管理后台'
admin.site.site_header = 'My_BLOG'

# admin.sit.register([Category,Tag,Post,Comment])
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 列表显示属性，list_display表示要显示哪些属性
    list_display = ('title_name', 'create_time', 'modified_time', 'category', 'author', 'tag_name', 'is_delete')

    # 修改编辑页面排版, 编辑页面显示
    # fields = ('title', 'create_time')
    fieldsets = (
        ('正文/标题 ', {'fields': ['title', 'content']}),
        ('时间', {'fields': ['create_time', 'modified_time'], 'classes': ['collapse']}),
        ('分类/标签', {'fields': ['category', 'tag', 'image'], 'classes': ['collapse']}),
        ('作者', {'fields': ['author']})
    )

    # 搜索框，根据title，category搜索
    search_fields = ['title', 'category']

    # 过滤，根据title，category过滤
    list_filter = ['title', 'category']

    # 每一页显示10
    list_per_page = 10


# 添加关联对象, 声明为 TabularInline 后内嵌的Post就以表格的形式展示
class PostInline(admin.TabularInline):
    model = Post
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    inlines = [PostInline]

    search_fields = ['category_name']