#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import hashlib
import urlparse
import sys


def scrapeQuora(category):
    url = "http://www.quora.com/%s/rss"%category
    soup = BeautifulSoup( urllib2.urlopen(url).read(), 'xml' )
    arr =[]
    for q in soup.find_all("item"):
        d = {}
        d['title'] = q.find('title').get_text()
        d['link'] = q.find('link').get_text()
        arr.append(d)

    return arr

def addFeed(interests):
    if not interests:
        interests = 'physics,maths'
    length = len(interests.split(","))

    if 'physics' in interests:
        arr.append(get_data('Physics', length))
        #arr.append(scrapeQuora('Physics'))
    if 'chemistry' in interests:
        arr.append(get_data('Chemistry', length))
    if 'math' in interests:
        arr.append(get_data('Mathematics', length))
    if 'biology' in interests:
        arr.append(get_data('Biology-1', length))

    return json.dumps(arr)

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


class FeedDB():
    file_name = 'feed.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # create new db and make connection
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS feed (count INTEGER PRIMARY KEY AUTOINCREMENT, \
                title TEXT, url TEXT UNIQUE, \
                image TEXT default '',\
                description TEXT default '',\
                featured BOOLEAN default False)''')
        self.conn.commit()

    
    def add_to_db(self,title,url,image='',description='',featured=False):
        self.c.execute(
            "INSERT or IGNORE INTO feed(title,url,image,description,featured) VALUES (?,?,?,?,?)",
            (title,url,image,description,featured))
        self.conn.commit()

    def exec_transaction(self,arr):
        self.c.executemany("insert or ignore into feed(title,url,image,description,featured) values (?,?,?,?,?)", arr)
        self.conn.commit()


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
    D = FeedDB()
    #print D.exec_query('Select * from posts')
    D.add_to_db('example title','http://imgur.caom/qrVUksea.jpg')
    V = VideosDB()
    print V.exec_query("Select * from video_db ORDER by RANDOM() limit 5")

if __name__ == '__main__':
    if sys.argv[1] == 'scrape':
        addFeed()    
    else:
        test()

