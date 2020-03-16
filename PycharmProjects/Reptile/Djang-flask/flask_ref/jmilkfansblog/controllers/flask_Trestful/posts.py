from flask_restful import Resource,fields,marshal_with
from jmilkfansblog.controllers.flask_Trestful import fields as jf_fields
from jmilkfansblog.controllers.flask_Trestful import parsers
from flask import abort,session
from jmilkfansblog.models import db,User,Post,Tag
from datetime import datetime

nested_tag_fields={
    'id':fields.Integer(),
    'name':fields.String()
}

nested_commit_fields={
    "id":fields.Integer(),
    'name':fields.String(),
    'text':jf_fields.HTMLField(),
    'datetime':fields.DateTime(dt_format='iso8601'),
    'post_id':fields.Integer()
}

posts_fields = {
    'id':fields.Integer(),
    'user_id':fields.Integer(),
    'author':fields.String(attribute=lambda x: x.users.username),
    'text':fields.String(),
    'title':jf_fields.HTMLField(),   # 字段值中的 HTML 标签过滤掉
    'tags':fields.List(fields.Nested(nested_tag_fields)),
    'publish_date':fields.DateTime(dt_format='iso8601'),
    'comments':fields.List(fields.Nested(nested_commit_fields)),
}


class PostsApi(Resource):

    @marshal_with(posts_fields)  # flask_restful 格式化输出
    def get(self,post_id=None):
        if post_id:
            post = Post.query.filter_by(id=post_id).first()
            if not post:
                abort(404)
            return post
        else:
            args = parsers.post_get_parser.parse_args()
            page = args['page'] or 1
            if args['user']:
                user = User.query.filter_by(username=args['user']).first()
                if not user:
                    abort(404)
                post = user.posts.order_by(Post.id.desc()).paginate(1,3)
            else:
                post = Post.query.order_by(Post.id.desc()).paginate(page,page+3)
            return post.items

    def post(self,post_id=None):
        if post_id:
            abort(400)
        else:
            args = parsers.post_post_parser.parse_args(strict=True)
            token = args['token']
            user = User.verify_auth_token(token)
            if not user:
                abort(401)
            new_post = Post('title')
            new_post.title = args['title']
            new_post.text = args['text']
            new_post.publish_date = datetime.now()
            new_post.users = user 

            if args['tags']:
                for item in args['tags']:
                    tag = Tag.query.filter_by(name=item).first()
                    if tag:
                        new_post.tags.append(tag)
                    else:
                        new_tag = Tag(item)
                        new_tag.name = item
                        new_post.tags.append(new_tag)
        db.session.add(new_post)
        db.session.commit()
        return (new_post.id,201)

        # if post_id:
        #     return {'post_id':post_id}
        # return {'hello':'world'}

    def put(self,post_id=None):
        if not post_id:
            abort(401,'update must take id')
        args = parsers.post_put_parser.parse_args()
        title = args['title']
        text = args['text']
        tags = args['tags']
        token = args['token']
        user = User.verify_auth_token(token)
        if not user:
            abort(401,'token is not right')
        posts = Post.query.get_or_404(post_id)
        # posts = Post.query.filter_by(id=post_id).first()
        if not posts or posts.users != user:
            abort(401,'post is not exist or not have Permission')
        if title:
            title = title
        text = text if text else posts.title
        posts.publish_date = datetime.now()
        if tags:
            for item in tags:
                tag = Tag.query.filter_by(name=item).first()
                if tag: 
                    if tag not in posts.tags:
                        posts.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    posts.tags.append(new_tag)
        db.session.add(posts)
        db.session.commit()
        return (posts.id,201)

    def delete(self,post_id=None):
        if not post_id:
            abort(401)
        
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404,'post is not exists')

        args = parsers.post_delete_parser.parse_args(strict=True)
        token = args['token']   
        # print(type(user),user,type(post.users))
        user = User.verify_auth_token(token)
        # db.session.refresh(u)
        # db.session.expunge(u)
        if not user:
            abort(401,'token is not right')
        user=db.session.merge(user)  # 模型对象不在当前的session中，通过db.session.merge或者db.session.add把模型添加到当前session中
        #  session已经被提交，导致操作的 model 对象已经不在当前 session 中了。 解决的办法就是：把对象重新加入到当前 session 中:

        # db.session.add(u)
        # if not uid:
        #     abort(401,'token is not right')
        # user = User.query.get_or_404(uid)
        # print(u.id)
        # print(u in db.session)
        # print(user in db.session)
        # print(type(user),uid,type(post.users))   
    
        if post.users != user:
            abort(403,'not have Permission')

        db.session.delete(post)
        db.session.commit()
        return ('success',204)