from django import template
register = template.Library()
# 为了成为一个可用的过滤器模块，这个模块必须包含一个名为 register的变量，
# 它是template.Library 的一个实例，所有的标签和过滤器都是在其中注册的。所以过滤器模块需要包含上面两行代码。


# 自定义过滤器，在模板templatetags 中{% load %} 声明调用
@register.filter    # 使用过滤器注册的方式，过滤器名为函数名
def mod(value, arg):  # 过滤器第一个参数是模板变量，第二个参数是接收开发人员传过来的参数
                         # 自定义过滤器开发人员只能传一个参数。
    return value % arg