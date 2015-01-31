#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask, flask.views
from flask import session, g, redirect, render_template, request, url_for, abort, flash
import urllib2
from flask_oauth import OAuth
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from models import *
import json, os, random, sqlite3
# from dbHelper import VideosDB
from settings import *
from credentials import *
import search
from flask_oauth import OAuth

CURR_PATH = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(CURR_PATH + '/videos.db', check_same_thread=False)
c = conn.cursor()

# from scraper import DB,chanell_names
from bs4 import BeautifulSoup
import urllib
import requests

# orig_chan_name = []
# fake_chan_name = []

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

# for i in chanell_names.split(','):
#     orig_chan_name.append(i.split(':')[0].lower())
#     fake_chan_name.append(i.split(':')[1])

@app.route('/')
def home():
    return flask.render_template('homepage.html')

# @app.route('/feed',methods=['GET'])
# def feed():
#     arr = Feed.Query.all().limit(50)
#     vids = None
#     #vids = VideosDB.get5()
#     #vids += VideosDB.get5ted()
#     return flask.render_template('feed.html', arr=arr, vids=vids)


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
def giveaway_home():
    arr = Post.Query.filter(is_deleted=0)
    return flask.render_template('giveaway.html', arr=arr)

@app.route('/giveaway/upload')
def giveaway_upload():
    return flask.render_template('upload.html')

@app.route('/giveaway/add',methods=['GET'])
def giveaway_add():
    post_content = request.args.get('post_content')
    user_id = request.args.get('user_id')
    if 0 < len(post_content) < 140:
        post = Post(content=post_content, user_id=user_id, is_deleted=0, )
        post.save()
    else:
        pass
        # flash an error message
    return flask.redirect("/giveaway#sa")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    username = request.form.get('user_name')
    institution = request.form.get('institute')
    email = request.form.get('user_email')
    passwd = request.form.get('user_password')
    authData = request.form.get('authData')
    #authData = "{"+authData+"}"
    #print authData
    #print json.loads(authData)
    u = User.signup(username=username, password=passwd, NAME=name,  INSTITUTE=institution, email=email)
    return redirect('/')

@app.route('/register')
def register():
    if session['oauth_token'][0] is not None:
        return redirect('/')
    return flask.render_template('register.html')

@app.route('/login/facebook')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    print session['oauth_token']
    me = facebook.get('/me')
    # print "yo"
    # print me.data
    # return 'Logged in as id=%s name=%s redirect=%s' % \
    #     (me.data['id'], me.data['name'], "http://localhost:8888/giveaway")
    return redirect(url_for('home'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

# @app.route('/login/submit', methods=['POST'])
# def login_submission():
#     username = request.form.get('user_name')
#     passwd = request.form.get('user_password')
#     u = User.login(username, passwd)
#     arr = Feed.Query.all().limit(50)
#     return flask.render_template('feed.html', u=u, arr=arr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
