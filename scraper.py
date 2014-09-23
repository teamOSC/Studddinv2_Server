#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sqlite3
import urllib
import urllib2
import logging

conn = sqlite3.connect('videos.db',check_same_thread=False)
c = conn.cursor()
cursor=conn.cursor()

chanell_names = 'MIT:MIT,khanacademy:Khan Academy,nptelhrd:NPTEL HRD,1veritasium:Veritasium,vsauce:V-Sauce,CGPGrey:CGP Grey,minutephysics:Minute Physics,destinws2:destin WS,scishow:Sci Show,crashcourse:Crash Course,AsapSCIENCE:Asap Science,numberphile:Numberphile,TheBadAstronomer:The Bad Astronomer,ACDCLeadership:ACDC Leadership,arinjayjain1979:Arinjay Jain,smithsonianchannel:Smithsonian Channel,historychannel:History Channel,periodicvideos:Periodic Videos,sixtysymbols:Sixty Symbols,Computerphile:Computerphile,FavScientist:Fav Scientist,coursera:Coursera,TEDxTalks:TedxTalks,bkraz333:BkRaz333,virtualschooluk:Virtual School UK,SpaceRip:Space RIP,bozemanbiology:BozeMan Biology,MindsetLearn: Mindset Learn,Mathbyfives:Math by Fives,jayates79:JayaTes79,MathTV:MathTV'

orig_chan_name = []
fake_chan_name = []
for i in chanell_names.split(','):
    orig_chan_name.append(i.split(':')[0].lower())
    fake_chan_name.append(i.split(':')[1])


def search(query):
    result_arr = []
    if query == '*':
        sql = "select * from video_db"
    else:
        sql = "select * from video_db where title LIKE '%%%s%%'"%(query)
    cursor.execute(sql)
    for row in cursor:
        result_arr.append(row)

    return result_arr

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS video_db
                 (id TEXT PRIMARYKEY,title TEXT, url TEXT ,img_url TEXT, chanell TEXT,rating REAL)''')
    conn.commit()
    #conn.close()

def add_to_db(v_id,title,url,img_url,chanell,rating):
    c.execute("INSERT INTO video_db VALUES (?,?,?,?,?,?)",(v_id,title,url,img_url,chanell,rating))
    conn.commit()
    #conn.close()

#array of already scraped videos
video_array = search('*')
video_url_array = [i[2] for i in video_array]

#returns array of all video urls in that chanell
def scrape_chanell(author):
    print '/***************\n%s\n***************/'%author
    arr=[]
    foundAll = False
    ind = 1
    videos = []
    while not foundAll:
        inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?start-index={0}&max-results=50&alt=json&orderby=published&author={1}'.format( ind, author ) )
        try:
            resp = json.load(inp)
            inp.close()
            returnedVideos = resp['feed']['entry']
            for video in returnedVideos:
                videos.append( video )

            ind += 50
            #print len( videos )
            if ( len( returnedVideos ) < 50 ):
                foundAll = True
        except:
            #catch the case where the number of videos in the channel is a multiple of 50
            print "error"
            foundAll = True
            logging.exception('foo')

    for video in videos:
        url = video['link'][0]['href']
        arr.append(url)
        #print video['title']

    arr = [i for i in arr if i not in video_array]
    return arr

def scrape_video_details(url):
    v_id = url.split('watch?v=')[-1]
    v_id = v_id.split('&')[0]
    gdata_url = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&prettyprint=true&alt=jsonc'%v_id
    response = urllib2.urlopen(gdata_url)
    html = response.read()
    data = json.loads(html)['data']

    title = data['title']
    img_url = data['thumbnail']['sqDefault']
    description = data['description']
    chanell = data['uploader']
    try:
        rating = data['rating']
    except KeyError:
        rating = 0

    add_to_db(v_id,title,url,img_url,chanell,rating)

    print v_id

def main():
    e = 0
    for chanell in orig_chan_name:
        arr = scrape_chanell(chanell)
        for url in arr:
            try:
                scrape_video_details(url)
            except:
                logging.exception('foo')
                print 'error adding video'
                e += 1
    print e

if __name__ == '__main__':
    main()
