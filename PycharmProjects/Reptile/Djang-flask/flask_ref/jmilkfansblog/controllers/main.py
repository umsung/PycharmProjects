from flask import Blueprint,flash,redirect,render_template,url_for
from jmilkfansblog.extensions import openid
from jmilkfansblog.forms import LoginForm,OpenIDForm,RegisterForm
from flask_login import login_user,logout_user
from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app
from jmilkfansblog.models import User,db
from uuid import uuid4

ad = Blueprint(
    'main',
    '__name__',
    template_folder='templates/admin',
    static_folder='static/admin',
    url_prefix='/main')


@ad.route('/')
def home():
    return render_template('home.html')


@ad.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(5,form.username.data,form.password.data)
        # user.id = str(uuid4)

        db.session.add(user)
        db.session.commit()
        flash('you user has beed register',category='success')
        return redirect(url_for('main.login'))
    
    return render_template('main/register.html',form=form)



@ad.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
    """View function for login.

       Flask-OpenID will be receive the Authentication-information
       from relay party.
    """

    # Create the object for LoginForm
    form = LoginForm()
    # Create the object for OpenIDForm
    openid_form = OpenIDForm()

    # Send the request for login to relay party(URL).
    if openid_form.validate_on_submit():
        return openid.trg_login(
            openid_form.openid_url.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname'])

    # Try to login the relay party failed.
    openid_errors = openid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    # Will be check the account whether rigjt.
    if form.validate_on_submit():

        # Using session to check the user's login status
        # Add the user's name to cookie.
        # session['username'] = form.username.data

        user = User.query.filter_by(username=form.username.data).one()

        # Using the Flask-Login to processing and check the login status for user
        # Remember the user's login status. 
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id))

        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))

    return render_template('main/login.html',
                           form=form,
                           openid_form=openid_form)


@ad.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    # Remove the username from the cookie.
    # session.pop('username', None)

    # Using the Flask-Login to processing and check the logout status for user.
    logout_user()

    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())
    flash("You have been logged out.", category="success")
    return redirect(url_for('main.login'))