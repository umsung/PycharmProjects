from django.contrib import admin
from django.urls import path
from personal_blog import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'title/', views.title, name='title'),
    # url(r'abc/(\w+)/', views.param),
    # url(r'save/(\w+)//(\w+)/(\w+)', views.save),
    url(r'^info/$', views.info),
    url(r'^method1/$', views.method1),
    url(r'^method2/$', views.method2),
    url(r'^method3$', views.method3),
    url(r'^meta/$', views.meta),
    url(r'^get/$', views.get),
    url(r'^get1/$', views.get1),
    url(r'^get2/$', views.get2),
    url(r'^post/$', views.post),
    url(r'^post1/$', views.post1),
    url(r'^resp/$', views.resp),
    url(r'^set_cookies/$', views.set_cookies),
    url(r'^get_cookies/$', views.get_cookies),
    url(r'^json/$', views.json),
    url(r'^login/$', views.login),
    url(r'^session/$', views.set_session),
    url(r'^var/$', views.var),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^base/$', views.base),
    url(r'^index/(\d+)/$', views.index, name='index'),
    url(r'^detail/(\d+)/', views.detail, name='detail'),
    url(r'^uploadImg/$', views.pic_upload, name='pic_upload'),
    url(r'^paginator/(\d+)/$', views.paginator, name='paginator'),
    url(r'^register/$', views.register, name='register'),
    url(r'^check_name/$', views.check_name),
    url(r'^search/$', views.search),
    url(r'^edit/(\d+)/$', views.edit, name='edit'),
    url(r'^edit_action/(\d+)/$', views.edit_action, name='edit_action')


]