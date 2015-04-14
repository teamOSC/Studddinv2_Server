#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import hashlib
import urlparse
import sys
from bs4 import BeautifulSoup
import urllib2
from models import Feed

def scrapeQuora():
    cat_string = 'Physics,Chemistry,Mathematics,Biology-1,Geography,Economics,History'
    cat_arr = cat_string.split(',')
    for category in cat_arr:
        url = "http://www.quora.com/%s/rss"%category
        print url
        if category == 'Biology-1':
            category = 'Biology'
        soup = BeautifulSoup( urllib2.urlopen(url).read(), 'xml' )

        for q in soup.find_all("item"):
            title = q.find('title').get_text()
            print title
            link = q.find('link').get_text()
            f = Feed(title=title,url=link,\
                image='http://rachelhoweconsulting.com/wp-content/uploads/2011/08/Rachel-Howe-on-Quora.png',\
                category=category)
            f.save()


class VideosDB():
    file_name = 'videos.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
        self.c = self.conn.cursor()

    def get5(self):
        return self.exec_query("Select * from video_db ORDER by RANDOM() limit 5")

    def get5ted(self):
        return self.exec_query("Select * from video_db where chanell like '%ted%' ORDER by RANDOM() limite 5")

    def exec_query(self, query):
        result_arr = []
        try:
            self.c.execute(query)
            self.conn.commit()
            for row in self.c:
                result_arr.append(row)
        except:
            result_arr = []
        return result_arr


def test():
    V = VideosDB()
    print V.exec_query("Select * from video_db ORDER by RANDOM() limit 5")

if __name__ == '__main__':
    if sys.argv[1] == 'scrape':
        scrapeQuora()   
    else:
        test()

