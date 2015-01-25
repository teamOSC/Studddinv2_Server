#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask, flask.views
app = flask.Flask(__name__)
import urllib2

from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from models import *
from flask import render_template, request, url_for, abort, g, flash
import json
import os
import random, sqlite3
import grequests
from dbHelper import FeedDB,VideosDB

CURR_PATH = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(CURR_PATH + '/videos.db',check_same_thread=False)
c = conn.cursor()

from scraper import DB,chanell_names
from bs4 import BeautifulSoup
import urllib
import requests

orig_chan_name = []
fake_chan_name = []
count = 0
so_numbers = dict()

for i in chanell_names.split(','):
    orig_chan_name.append(i.split(':')[0].lower())
    fake_chan_name.append(i.split(':')[1])

def get_original_image(thumbnail_url):
    #orig = thumbnail_url.replace('/thumb','')
    orig = '/'.join(thumbnail_url.split('/')[:-1])
    f = orig.split('/')[-1]
    if '.ogv' in orig:
        p = '/mid-'
    else:
        p = '/200px-'
    orig = orig + p +f
    if orig.endswith('.svg'):
        orig = orig + '.png'
    elif '.ogv' in orig:
        #orig.replace('/200px','/mid')
        orig = orig + '.jpg'
    return orig

def scrape_wiki(query):
    url = 'http://en.wikipedia.org/w/api.php?action=opensearch&limit=10&format=xml&search=%s&namespace=0'%(query)
    soup = BeautifulSoup( urllib2.urlopen(url).read(), 'xml')
    arr =[]
    for q in soup.find_all("Item"):
        try:
            d={}
            d['title'] = q.Text.get_text()
            img = q.Image.get('source')
            d['img'] = get_original_image(img)
            d['url'] = q.Url.get_text()
            arr.append(d)
        except:
            pass
    return arr

def stackoverflow_api(query):
    sites = [
        "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&site=math"%query,
        "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&site=chemistry"%query,
        "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&site=physics"%query,
        "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&site=biology"%query
    ]
    async_list = []

    for site in sites:
        action_item = grequests.get(site, hooks = {'response' : get_so_api_data})
        async_list.append(action_item)

    grequests.map(async_list)

def get_so_api_data(api_data, **kwargs):
    elements = api_data.json()
    global count
    if len(elements["items"]) > count:
        global count
        count = len(api_data.json()["items"])
        global so_numbers
        so_numbers = elements

def youtube_api(query):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyD05WKF7JQ1hHmkgxb2L47OzApqaSy0pH8&q=%s"%query
    json = requests.get(url).json()
    return json["items"]

def reddit_api(query):
    headers = {
        'User-Agent': 'Acadsurf',
        'From': 'stomatrix@gmail.com'  # This is another valid field
    }
    url = "http://www.reddit.com/search.json?q=%s"%query
    json = requests.get(url,headers=headers).json()
    return json["data"]["children"]


@app.route('/')
def home():
    return flask.render_template('homepage.html')
    
@app.route('/feed',methods=['GET'])
def feed():
    arr = Feed.Query.all().limit(50)
    return flask.render_template('feed.html', arr=arr)


@app.route('/search.json')
def SearchApi():
    q = request.args.get('q') or 0

    if not q:
        return "{'status':400,\n\t'response':'query(q) is a required parameter'}"

    wiki_data = scrape_wiki(q)
    youtube_data = youtube_api(q)
    reddit_data = reddit_api(q)
    stackoverflow_api(q)
    global so_numbers
    so_data = so_numbers

    return json.dumps({
       'wiki_data':wiki_data,
       'youtube_data':youtube_data,
       'reddit_data':reddit_data,
       'so_data':so_data,
    }, indent=4)
    
    
@app.route('/search')
def Search():
    q = request.args.get('q') or 0

    if not q:
        return "{'status':400,\n\t'response':'query(q) is a required parameter'}"

    wiki_data = scrape_wiki(q)
    youtube_data = youtube_api(q)
    reddit_data = reddit_api(q)
    stackoverflow_api(q)
    global so_numbers
    so_data = so_numbers
    return flask.render_template('index.html',wiki_data=wiki_data,youtube_data=youtube_data,reddit_data=reddit_data,so_data=so_data)

@app.route('/giveaway', methods=['GET'])
def giveaway_home():
    arr = Post.Query.filter(is_deleted=0)
    return flask.render_template('giveaway.html', arr=arr)

@app.route('/giveaway/add',methods=['GET'])
def giveaway_add():
    post_content = request.args.get('post_content')
    user_id = request.args.get('user_id')
    if 0 < len(post_content) < 140:
        post = Post(content=post_content, user_id=user_id, is_deleted=0)
        post.save()
    else:
        pass
        # flash an error message
    return flask.redirect("/#sa")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
