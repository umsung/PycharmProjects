from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Category(models.Model):
    # 分类名
    category_name = models.CharField(max_length=20)

    def __str__(self):  # __unicode__ on Python 2
        return self.category_name

    class Meta:
        verbose_name_plural = '分类'
        # db_table = 'Students'


class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):     # __unicode__ on Python 2
        return self.tag_name

    class Meta:
        verbose_name_plural = '标签'


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 表示外键关联到分类表,当分类表删除中关联字段删除后,文章表中不删除,仅仅是把外键置空
    # 分类，使用外键连接 一对多关系使用ForeignKey
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField(Tag, blank=True)  # 标签，多对多关系使用ManyToManyField
    is_delete = models.BooleanField(default=False)  # 逻辑删除字段
    # 表示外键关联到作者表中,当作者表中关联字段删除后,文章表中将关联数据删除。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')


    def __str__(self):     # __unicode__ on Python 2
        # Post列表返回title
        return self.title

    def tag_name(self):
        # tag标签是ManyToManyField类型，在模型类中添加方法
        return ','.join([str(i) for i in self.tag.all()])

    # 修改列表显示标题
    def title_name(self):
        return self.title
    title_name.short_description = '标题'

    class Meta:
        verbose_name_plural = '文章'   # 修改表名
        ordering = ['-create_time']    # 以创建时间倒序显示结果


class Comment(models.Model):
    name = models.CharField(max_length=10)
    content = models.TextField()
    time = models.DateTimeField()
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):     # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = '评论'