import grequests
import flask, flask.views
from flask import session, g, redirect, render_template, request, url_for, abort, flash
import urllib2
import json
#from scraper import DB,chanell_names
from bs4 import BeautifulSoup
import urllib
import requests

count = 0
so_numbers = dict()

def get_dict(**kwargs):
    d= {}
    for k,v in kwargs.iteritems():
        d[k] = v
    return d

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
    arr = []
    for i in json['items']:
        img = i['snippet']['thumbnails']['medium']['url']
        title = i['snippet']['title']
        video_id = i['id']['videoId']
        url = "https://www.youtube.com/watch?v=%s"%video_id
        d = get_dict(img=img,title=title,url=url)
        arr.append(d)
    return arr

def reddit_api(query):
    headers = {
        'User-Agent': 'Acadsurf',
        'From': 'stomatrix@gmail.com'  # This is another valid field
    }
    url = "http://www.reddit.com/search.json?q=%s"%query
    json = requests.get(url, headers=headers).json()
    arr = []
    for i in json["data"]["children"]:
        if i['data']['over_18']: continue
        title = i['data']['title']
        img = i['data']['thumbnail']
        if img == 'self':
            img = "http://png-4.findicons.com/files/icons/1982/social_me/60/reddit.png"
        url = i['data']['url']
        d = get_dict(img=img,title=title,url=url)
        arr.append(d)

    return arr


def get_so_data(query):
    stackoverflow_api(query)
    global so_numbers
    return so_numbers