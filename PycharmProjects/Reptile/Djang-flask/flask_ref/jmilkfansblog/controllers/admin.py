"""后台
ModelView: 模型视图
FileAdmin: 本地文件系统管理
BaseView: 基础视图
"""
from flask_admin import BaseView,expose
from flask_admin.contrib.sqla import ModelView
from jmilkfansblog.forms import CKTextAreaField,CKTextAreaWidget
from flask_admin.contrib.fileadmin import FileAdmin
from jmilkfansblog.extensions import admin_permission
from flask_login import current_user,login_required

class CustomView(BaseView):

    @expose('/')    
    @admin_permission.require(http_exception=403)
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page.html')

class CustomModelView(ModelView):
    """File System admin."""
    # def is_accessible(self):
    #     """Setup the access permission for CustomModelView."""

    #     # callable function `User.is_authenticated()`.
    #     # FIXME(JMilkFan): Using function is_authenticated()
    #     return current_user.is_authenticated and admin_permission.can() 



class PostView(CustomModelView):
    """View function of Flask-Admin for Post create/edit Page includedin Models page"""

    # Using the CKTextAreaField to replace the Field name is `test`
    form_overrides = dict(text=CKTextAreaField)

    # Using Search box
    column_searchable_list = ('text', 'title')

    # Using Add Filter box
    column_filters = ('publish_date',)

    # Custom the template for PostView
    # Using js Editor of CKeditor
    create_template = 'admin/post_edit.html'
    edit_template = 'admin/post_edit.html'

class CustomFileView(FileAdmin):
    """File System admin."""

    # def is_accessible(self):
    #     return current_user.is_authenticated and admin_permission.can()


