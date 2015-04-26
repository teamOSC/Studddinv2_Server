from flask import Flask,render_template, flash, redirect, \
make_response,request, url_for , session, g, jsonify

from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user

from oauth import OAuthSignIn
import search

from models import Feed,Notes

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

class LocalUser(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return LocalUser.query.get(int(id))


@app.route('/')
def landing():
    return render_template('landingpage.html')

@app.route('/home')
def home():
    resp = Feed.Query.all()
    return render_template('index.html', data=resp)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


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
    
    return redirect(url_for('home'))


@app.route('/notes')
def notes():
    notes = Notes.Query.all()
    return render_template('notes.html', notes=notes)


@app.route('/notes/upload')
def notesUpload():
    notes = Notes.Query.all()
    return render_template('notes.html', notes=notes)


@app.route('/notes/<objID>')
def viewNotes(objID): 
    notes = Notes.Query.get(objectId=objID)
    return render_template('notes.html', notes=notes)

@app.route('/api/feed')
def Feed():
    q = 'fruits'
    wiki_data = search.scrape_wiki(q)
    youtube_data = search.youtube_api(q)
    reddit_data = search.reddit_api(q)
    #so_data = search.get_so_data(q)

    resp = jsonify(data={
       'wiki_data':wiki_data,
       'youtube_data':youtube_data,
       'reddit_data':reddit_data,
    })
    resp.status_code = 200
    return resp


@app.route('/api/search')
def SearchApi():
    q = request.args.get('q') or 0

    if not q:
        resp = jsonify(data={"GET request param q not specified"})
        resp.status_code = 500
        return resp
        

    wiki_data = search.scrape_wiki(q)
    youtube_data = search.youtube_api(q)
    reddit_data = search.reddit_api(q)
    #so_data = search.get_so_data(q)

    resp = jsonify(data={
       'wiki_data':wiki_data,
       'youtube_data':youtube_data,
       'reddit_data':reddit_data,
    })
    resp.status_code = 200
    return resp
