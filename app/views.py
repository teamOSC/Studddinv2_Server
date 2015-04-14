from flask import Flask,render_template, flash, redirect, make_response,request, url_for , session, g

from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user

from oauth import OAuthSignIn
from models import LocalUser


db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    try:
        user = LocalUser.query.filter_by(social_id=social_id).first()
    except:
        user = ''
        db.create_all()

    if not user:
        user = LocalUser(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    
    return redirect(url_for('index'))


