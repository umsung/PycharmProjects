from flask_wtf import FlaskForm
# from FlaskForm import Form
from wtforms import widgets,StringField, TextField, TextAreaField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, URL
from jmilkfansblog.models import User,db

'''WTForms：是一个服务端表单检验库，用于在保证安全的前提下，对常见的表单类型进行输入的合法性验证。
除此之外，还提供了 Jinja HTML 渲染、预防跨域请求伪造(CSRF)、SQL 注入。
'''



class CKTextAreaWidget(widgets.TextArea):

    def __call__(self,field,**kwargs):

        kwargs.setdefault('class_','cheditor')
        return super(CKTextAreaWidget,self).__call__(field,**kwargs)

class CKTextAreaField(TextAreaField):
    """create n new Field"""

    widget = CKTextAreaWidget()


class CommentForm(FlaskForm):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField('Name',validators=[DataRequired(), Length(max=5)])

    text = TextField(u'Comment', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username',[DataRequired(),Length(5)])
    password= PasswordField('Password',[DataRequired(),Length(min=6)])
    comfirm = PasswordField('confirm Password',[DataRequired(),Length(min=6),EqualTo('password')])
    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm,self).validate()
        if not check_validate:
            return False
        
        user = db.session.query(User).filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('user already exist')
            return False
        return True



'''用户登陆表单'''
class LoginForm(FlaskForm):
    username = StringField('Username',[DataRequired(),Length(5)])
    password= PasswordField('Password',[DataRequired()])
    remember = BooleanField('Remember me')

    def validate(self):
        """重载父类的检验函数 validate()，扩展了个性化的检验需求.
        检验函数 validate()会在表单对象From调用 validate_on_submit() 的时候被调用
        """
        check_validate = super(LoginForm,self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid username or password.')
            return False
        
        return True

class PostForm(FlaskForm):
    title = StringField('Title',[DataRequired(),Length(max=10)])
    text = TextAreaField('Text',[DataRequired(),Length(max=255)])


class OpenIDForm(FlaskForm):
    """OpenID Form."""

    openid_url = StringField('OpenID URL', [DataRequired(), URL()])