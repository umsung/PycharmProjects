from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from personal_blog.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import cache_page
#
#
def test(request):
    post = Post.objects.all()  # 获取Post列表
    content = [i for i in post]
    return HttpResponse(content)


def title(request):
    post_title = Post.objects.all()

    # # 1加载模板
    # template = loader.render_to_string("personal_blog/title.html", {"post_title": post_title}, request)
    # return HttpResponse(template)

    return render(request, 'personal_blog/title.html', context={'post_title': post_title})


# def param(request, tag):
#     post = Post.objects.get(title=tag)
#     post.delete()
#
#     return HttpResponse('{}被删除了'.format(tag))


# def save(request, title, c_time, m_time):
#     post = Post()
#     post.title = title
#     post.create_time = c_time
#     post.modified_time = m_time
#     post.save()
#     return HttpResponse('ok')


def info(request):
    a = '请求协议：{}，</br>请求路径：{}，</br>请求编码：{}'.format(request.method, request.path, request.encoding)

    return HttpResponse(a)


def method1(request):
    return render(request, 'personal_blog/method1.html')


def method2(request):
    return HttpResponse(request.method)


def method3(request):
    return HttpResponse(request.method)


def meta(request):
    m = request.META
    stri = ''

    for k, y in m.items():
        stri += '{} : {}'.format(k, y) + '</br>'
    return HttpResponse(stri)


def get(request):
    return render(request, 'personal_blog/get.html')


def get1(request):
    dict1 = request.GET  # 获取get请求的参数，返回一个QueryDict对像
    a = dict1.get('a')
    b = dict1.get('b')
    c = dict1.get('c', '默认值D')
    d = dict1.get('d')
    return HttpResponse('a: {}, b: {}, c:{}, d:{}'.format(a, b, c, d))


def get2(request):
    dict2 = request.GET
    a = dict2.getlist('a')
    b = dict2.getlist('b', '默认值getlist')
    return HttpResponse('a: {}, b: {}'.format(a, b))


def post(request):
    return render(request, 'personal_blog/post.html')


def post1(request):
    dict1 = request.POST
    uname = dict1.get('uname')
    upwd = dict1.get('upwd')
    ugender = dict1.get('ugender')
    uhobby = dict1.getlist('uhobby')
    context = {'uname': uname, 'upwd': upwd, 'ugender': ugender, 'uhobby': uhobby}

    return render(request, 'personal_blog/post1.html', context=context)

# def post1(request):
#     dict1 = request.POST
#     a = dict1.post


def resp(request):
    response = HttpResponse(content='aaa', status=300)
    print(response.status_code)
    return response


def set_cookies(request):
    response = HttpResponse('shezhi.............')
    response.set_cookie('username', 'admin')
    response.set_cookie('password', '123456', max_age=60*60*12)  # 设置超时时间 60*60*12秒
    return response


def get_cookies(request):
    cookie = request.COOKIES
    username = cookie.get('username')
    password = cookie.get('password')
    response = HttpResponse('{}: {}'.format(username, password))  # 将获取到的cookie返回
    return response


def json(request):
    return JsonResponse({'duan': 'test'})


def login(request):
    username = 'duan'
    password = '123456'
    if request.method == 'GET':
        return render(request, 'personal_blog/login.html')
    elif request.method == 'POST':
        dict = request.POST
        uname = dict.get('username')
        upwd = dict.get('password')
        if uname == username and upwd == password:
            return HttpResponseRedirect(reverse('title'))
        else:
            context = {'iserror': '错误', 'uname': uname, 'upwd': upwd}
            return render(request, 'personal_blog/login.html', context=context)
    # return HttpResponseRedirect()


def set_session(request):
    request.session['a'] = 'python'
    request.session['b'] = 'myweb'
    request.session['c'] = 'duan'
    request.session.set_expiry(60*60)
    return HttpResponse('test session')


def var(request):
    uname = {'name': 'duan'}
    pwd = ['123456']
    context = {'uname': uname, 'pwd': pwd}
    return render(request, 'personal_blog/var.html', context=context)


def tag(request):
    cg = Category.objects.all()
    context = {'category': cg}
    return render(request, 'personal_blog/tag.html', context=context)


def base(request):
    return render(request, 'personal_blog/base.html')


# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'personal_blog/index.html', context={'post_list': post_list})
#
#
# def detail(request):
#     post = Post.objects.get(id=4)
#     post2 = Post.objects.get(id=2)
#     html = '<h1>biaoqian</h1>'
#     h2 = '<h1>h2</h1>'
#     return render(request, 'personal_blog/detail.html', context={'post': post, 'post2': post2, 'html': html, 'h2': h2})


def pic_upload(request):
    if request.method == 'GET':
        return render(request, 'personal_blog/uploadImg.html')
    elif request.method == 'POST':
        pic = request.FILES.get('pic')  # HttpRequest 对象中的Files属性接收文件。以键值对的方式。

        f2 = FileSystemStorage()    # django自带的文件处理类，可以帮我们自动保存用户上传的文件。
        if pic is None:
            return HttpResponseRedirect('/uploadImg/')
        else:
            path = f2.save('blog/%s' %(pic.name), pic)  # 保存文件并返回文件名，如果文件名存在则会创建一个不重复的名称

            # 将上传的图片路径保存在 id为：'2' 的文章的image字段中。
            p = Post.objects.get(id=2)

            p.image = path

            p.save()

            return HttpResponse(pic.name)


# class IndexView(ListView):
#     model = Post
#     template_name = 'personal_blog/index.html'
#     context_object_name = 'post_list'
def index(request, page):
    from django.core.paginator import Paginator
    pos = Post.objects.all()
    a = Paginator(pos, 3)
    post_list = a.page(page)

    return render(request, 'personal_blog/index.html', context={'post_list': post_list})

# class MyDetailView(IndexView):
#
#     template_name = 'personal_blog/detail.html'
#     context_object_name = 'post'
#
#     def get_queryset(self):
#         return super(MyDetailView, self).get_queryset().get(id=self.args[0])


def detail(request, id):
    html = '<h1>我很帅</h1>'
    h2 = '<h1>我是真的很帅</h1>'
    post = Post.objects.get(id=id)
    return render(request, 'personal_blog/detail.html', context={'post': post, 'html': html, 'h2': h2})


@cache_page(60*15)
def paginator(request, index):
    from django.core.paginator import Paginator
    pos = Post.objects.all()
    a = Paginator(pos, 2)

    p = a.page(index)

    return render(request, 'personal_blog/paginator.html', context={'post_list': p})


def register(request):
    return render(request, 'personal_blog/register.html')


def check_name(request):
    name = request.POST.get('uname')
    upwd = request.POST.get('upwd')
    s_name = User.objects.filter(username=name)
    if s_name:
        return JsonResponse({'success': 1})
    else:
        return JsonResponse({'success': 0})


def search(request):
    dict1 = request.POST
    a = dict1.get('p')
    return render(request, 'personal_blog/search.html', context={'a': a})


def edit(request, id):
    if str(id) == '0':

        return render(request, 'personal_blog/edit.html', context={'id': id})
    else:

        post_list = Post.objects.get(id=id)
        # a = [i for i in post_list.objects.all()]
        # a = ','.join(a)
        return render(request, 'personal_blog/edit.html', context={'post_list': post_list, 'id': id})


def edit_action(request, id):
    from django.core.paginator import Paginator
    t = request.POST['t']
    content = request.POST['content']
    # create_time = request.POST['ctime']
    # modified_time = request.POST['mtime']
    # category = request.POST['category']
    # author = request.POST['author']
    # id = request.POST['id_hidden']
    if str(id) == '0':
        Post.objects.create(title=t, content=content, create_time='2019-1-22 16:48:08', modified_time='2019-1-22 16:48:08', author_id=1)
    # pos = Post.objects.all()
    # # a = Paginator(pos, 3)
    # # post_list = a.page(page)
    # return render(request, 'personal_blog/index.html', context={'post_list': pos})
        return HttpResponseRedirect('/index/1/')
    else:
        create_time = request.POST['ctime']
        modified_time = request.POST['mtime']
        category = request.POST['category']
        author = request.POST['author']
        p = Post.objects.get(id=id)
        p.title = t
        p.content = content
        p.create_time = create_time
        p.modified_time = modified_time
        p.category = Category.objects.get(id=2)
        # p.author = author
        p.save()
        return HttpResponseRedirect('/detail/{}'.format(id))


