from uuid import uuid4
from os import path
from datetime import datetime

from flask import render_template, Blueprint,redirect,url_for,render_template,flash,g
from sqlalchemy import func

from jmilkfansblog.models import db, User, Post, Tag, Comment, posts_tags
from jmilkfansblog.forms import LoginForm,RegisterForm

# os.path.pardir 表示上级目录
ah = Blueprint('auth',__name__,template_folder=path.join(path.pardir, 'templates', 'auth'))

@ah.route('/')
def index():
    return redirect(url_for('blog.home'))
    # return '111'

@ah.route('/login',methods=['GET','POST'])
def Login():
    From = LoginForm()
    if From.validate_on_submit():
        flash('you have been logged in',category='success')
        return redirect(url_for('blog.home'))
    return render_template('')


@ah.route('/register',methods=['GET','POST'])
def register():
    Form = RegisterForm()
    if Form.validate_on_submit():
        user = User(Form.username.data)
        user.password = Form.password.data
        user.id = str(uuid4)

        db.session.add(user)
        db.session.Comment()
        flash('you user has beed register',category='success')
        return redirect(url_for('blog.login'))
    
    return render_template('register.html',Form=Form)