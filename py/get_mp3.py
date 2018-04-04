# -*- coding:utf-8 -*-

import os
import sys
import io
import time
import requests
import urllib
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','referer':"http://www.ximalaya.com/swf/sound/red.swf"}

def create_soup(url):
    response = requests.get(url, headers = headers)
    # response.encoding = 'gb2312'
    return BeautifulSoup(response.text, 'html.parser')

def get_mp3_url(url):
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    msg = response.text

    mp3_url = msg.split("&play_url=")[1].split(".mp3&")[0]+".mp3"
    name = msg.split("&title=")[1].split("&nickname")[0]
    name = urllib.unquote(str(name)).decode('utf-8')
    name = name.decode('utf8')

    print mp3_url
    print name

    return mp3_url,name


def save_mp3(url, album_name, id, name):
    r = requests.get(url, headers = headers)
    name = "%s/%s_%s.mp3" % (album_name, id, name)
    print name
    with open(name, 'wb') as file:
        file.write(r.content)
    return True

def down_a_page(url, album_name):
    soup = create_soup(url)
    list1 = soup.find(class_ = "album_soundlist").find_all('li')
    count = 1000
    for msg1 in list1:
        count = count  + 1
        id = msg1.get('sound_id')
        print id

        url ="http://www.ximalaya.com/tracks/"+id+".ext.text"
        mp3_url, name = get_mp3_url(url)
        save_mp3(mp3_url, album_name, id, name)


def get_page_count(url):
    soup = create_soup(url)
    album_name = soup.find(class_ = 'detailContent_title').find_all('h1')[0].getText()
    print album_name
    album_name = "mp3/%s" % album_name
    if not os.path.exists(album_name):
        os.makedirs(album_name)

    list1 = soup.find(class_ = 'pagingBar').find_all('a')
    count = 0
    for msg1 in list1:
        count = count + 1 

    if(count>1):
        count = count - 1
    else:
        count = 1
    return count, album_name

def start(url):
    page_count, album_name = get_page_count(url)
    for index in range(page_count):
        page_url = '%s?page=%d' % (url, (index - 1))
        print page_url
        down_a_page(page_url, album_name)

url_list = [
    "http://www.ximalaya.com/54715628/album/4790468/",
    "http://www.ximalaya.com/96295838/album/12642897/",
    "http://www.ximalaya.com/44255360/album/5021722/",
    "http://www.ximalaya.com/29044178/album/11953680/",
    "http://www.ximalaya.com/44190264/album/5088879/",
]

for url in url_list:
    start(url)

