#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask, flask.views
from flask import session, g, redirect, render_template, request, url_for, abort, flash
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from models import *
import json, os, random, sqlite3, urllib, requests, urllib2
from dbHelper import VideosDB
from settings import *
from credentials import *
# import search
from flask_oauth import OAuth
from decorators import login_required, is_loggedin

CURR_PATH = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(CURR_PATH + '/videos.db', check_same_thread=False)
c = conn.cursor()

from scraper import DB,chanell_names
from bs4 import BeautifulSoup

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=fb_credentials["app_id"],
    consumer_secret=fb_credentials["app_secret"],
    request_token_params={'scope': 'email'}
)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='FfUOeQ5OBuv0qOkdHbfXCrwdk',
    consumer_secret='xQmFnUSii54eS3iUrl0uIrxfeL4EfIdFc6iyoHUDgSIVGDbauD'
)

@app.route('/')
@login_required
def index():
    return flask.render_template('homepage.html')

@app.route('/feed',methods=['GET'])
def feed():
    arr = Feed.Query.all().limit(50)
    vids = None
    #vids = VideosDB.get5()
    #vids += VideosDB.get5ted()
    return flask.render_template('feed.html', arr=arr, vids=vids)


# @app.route('/search.json')
# def SearchApi():
#     q = request.args.get('q') or 0

#     if not q:
#         return "{'status':400,\n\t'response':'query(q) is a required parameter'}"

#     wiki_data = search.scrape_wiki(q)
#     youtube_data = search.youtube_api(q)
#     reddit_data = search.reddit_api(q)
#     so_data = search.get_so_data(q)

#     return json.dumps({
#        'wiki_data':wiki_data,
#        'youtube_data':youtube_data,
#        'reddit_data':reddit_data,
#        'so_data':so_data,
#     }, indent=4)


# @app.route('/search')
# def Search():
#     q = request.args.get('q') or 0

#     if not q:
#         return "{'status':400,\n\t'response':'query(q) is a required parameter'}"

#     wiki_data = search.scrape_wiki(q)
#     youtube_data = search.youtube_api(q)
#     reddit_data = search.reddit_api(q)
#     so_data = search.get_so_data(q)
#     return flask.render_template('index.html',wiki_data=wiki_data,youtube_data=youtube_data,reddit_data=reddit_data,so_data=so_data)

@app.route('/giveaway')
@login_required
def giveaway_home():
    arr = Listings.Query.all()
    return flask.render_template('giveaway.html', arr=arr)


@app.route('/view/<string:obj_id>')
@login_required
def view_listing(obj_id):
    print obj_id
    obj = Listings.Query.filter(objectId=obj_id)

    return flask.render_template('view.html', obj=obj)


@app.route('/giveaway/upload')
@login_required
def giveaway_upload():
    return flask.render_template('upload.html')

@app.route('/giveaway/add',methods=['GET'])
@login_required
def giveaway_add():
    post_content = request.args.get('post_content')
    user_id = request.args.get('user_id')
    if len(post_content) < 140 and len(post_content)>0:
        post = Post(content=post_content, user_id=user_id, is_deleted=0, )
        post.save()
    else:
        pass
        # flash an error message
    return flask.redirect("/giveaway#sa")

@app.route('/register/submit', methods=['POST'])
def register_submit():
    name = request.form.get('name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    u = User.signup(username=email, password=password, email=email, NAME=name)
    u.save()
    session['oauth_token'] = (u.objectId,)
    return redirect('/')

@app.route('/register')
@is_loggedin
def register():
    return flask.render_template('register.html', next=request.args.get('next', None))

@app.route('/login/facebook')
def login_facebook():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next', None),
        _external=True))

@app.route('/login/twitter')
def login_twitter():
    return twitter.authorize(callback=url_for('twitter_authorized', next=request.args.get('next', None)))


@app.route('/login/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = User.Query.filter(email=me.data['email'])
    if not user:
        # authData = json.dumps({"facebook": {"id": me.data['id'], "access_token": resp['access_token']}})
        user = User.signup(username=me.data['email'], password="123456", email=me.data['email'])
    return redirect(next_url)

@app.route('/login/twitter/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['oauth_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    user = User.Query.filter(username=resp['screen_name'])
    if not user:
        user = User.signup(username=resp['screen_name'], password="123456")

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')

@app.route('/logout')
def logout():
    session['oauth_token'] = (None,)
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)