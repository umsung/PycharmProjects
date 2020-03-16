from flask_restful import reqparse
'''解析器 解析get请求获取请求的参数,用于查找和解析请求中所携带的参数.命名规则为 resourceName_functionName_parser'''

post_get_parser = reqparse.RequestParser()

post_get_parser.add_argument(
    'page',
    type=int,
    location=['json','args','headers'],
    required=False
)

post_get_parser.add_argument(
    'user',
    type=str,
    location=['json','args','header'],
    required=False
)

'''解析器 解析post请求获取请求参数'''
post_post_parser = reqparse.RequestParser()

post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Title is required'
)

post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help='text is required'
)

post_post_parser.add_argument(
    'tags',
    type=str,
    required=False,
    action='append'  # 指定了传入的参数会转换为以字典为元素的列表数据类型
)

post_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to create posts.'
)


post_put_parser=reqparse.RequestParser()

post_put_parser.add_argument(
    'title',
    type=str,
)

post_put_parser.add_argument(
    'text',
    type=str,
)

post_put_parser.add_argument(
    'tags',
    type=str,
    action='append'
)

post_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to update posts.'
)


post_delete_parser = reqparse.RequestParser()

post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Auth Token is required to update posts.'
)

user_post_parser = reqparse.RequestParser()

user_post_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='username is required'
)

user_post_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='password is required'
)