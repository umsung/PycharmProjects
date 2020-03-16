from django import http
from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):
    blacklist = ['120.196.164,25', '152.26.135.12']

    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in self.blacklist:  # request.META['REMOTE_ADDR'] 获取请求者的ip,判断这个用户ip是否在黑名单中。
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        print('--------------request')

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('--------------view')

    def process_template_response(self, request, response):
        print('--------------template')
        return response

    def process_response(self, request, response):
        print('--------------response')
        return response