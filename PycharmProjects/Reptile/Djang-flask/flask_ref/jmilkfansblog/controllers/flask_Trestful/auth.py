from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import abort,current_app
from flask_restful import Resource
from jmilkfansblog.controllers.flask_Trestful import parsers
from jmilkfansblog.models import User

class AuthApi(Resource):
    def post(self):
        try:
            args = parsers.user_post_parser.parse_args()
            user = User.query.filter_by(username=args['username']).first()

            if user and user.check_password(args['password']):
                serializer = Serializer(current_app.config['SECRET_KEY'],expires_in=600)

                return {'token':serializer.dumps({'id':user.id}).decode()}
            else:
                abort(401,'user or password is not right!')
        except Exception:
            return None