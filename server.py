#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask, flask.views
app = flask.Flask(__name__)
import urllib2

from flask import render_template
from flask import request
import json
import os

from scraper import DB,chanell_names
from bs4 import BeautifulSoup
import urllib
import requests

orig_chan_name = []
fake_chan_name = []
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
    url = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q=%s&site=math"%query
    json = requests.get(url).json()
    return json["items"]

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

def scrapeQuora(category):
    url = "http://www.quora.com/%s/rss"%category
    soup = BeautifulSoup( urllib2.urlopen(url).read() ,'xml' )
    arr =[]
    for q in soup.find_all("item"):
        d = {}
        d['title'] = q.find('title').get_text()
        d['link'] = q.find('link').get_text()
        arr.append(d)
    return arr

@app.route('/feed.json',methods=['GET'])
def feedApi():
    arr = []
    interests = request.args.get('interests') or ''
    if not interests:
        interests = 'physics,maths'

    if 'physics' in interests:
        arr.append(scrapeQuora('Physics'))
    if 'chemistry' in interests:
        arr.append(scrapeQuora('Chemistry'))
    if 'math' in interests:
        arr.append(scrapeQuora('Mathematics'))
    if 'biology' in interests:
        arr.append(scrapeQuora('Biology-1'))

    return json.dumps(arr)

@app.route('/feed',methods=['GET'])
def feed():
    arr = []
    interests = request.args.get('interests') or ''
    if not interests:
        interests = 'physics,maths'

    if 'physics' in interests:
        arr.append(scrapeQuora('Physics'))
    if 'chemistry' in interests:
        arr.append(scrapeQuora('Chemistry'))
    if 'math' in interests:
        arr.append(scrapeQuora('Mathematics'))
    if 'biology' in interests:
        arr.append(scrapeQuora('Biology-1'))
    arr = arr[0]
    return flask.render_template('feed.html',arr=arr)


@app.route('/search.json')
def SearchApi():
    q = request.args.get('q') or 0

    if not q:
        return "{'status':400,\n\t'response':'query(q) is a required parameter'}"

    wiki_data = scrape_wiki(q)
    youtube_data = youtube_api(q)
    reddit_data = reddit_api(q)
    so_data = stackoverflow_api(q)

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
    so_data = stackoverflow_api(q)

    return flask.render_template('index.html',wiki_data=wiki_data,youtube_data=youtube_data,reddit_data=reddit_data,so_data=so_data)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
