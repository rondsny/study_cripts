# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import time


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','referer':"http://www.ximalaya.com/swf/sound/red.swf"}


def create_soup(url):
    response = requests.get(url, headers = headers)
    # response.encoding = 'gb2312'
    return BeautifulSoup(response.text, 'html.parser')

def get_mp3_url(url):
    response = requests.get(url, headers = headers)
    # response.encoding = 'gb2312'
    msg = response.text
    print response.url
    print response.text
    print response.status_code

    mp3_url = msg.split("&play_url=")[1].split(".mp3&")[0]+".mp3"
    print mp3_url
    return mp3_url
    

def save_mp3(url, count):
    r = requests.get(url, headers = headers)
    name = "reader3/%d.mp3" % (count)
    with open(name, 'wb') as file:
        file.write(r.content)
    return True

def test(url):
    soup = create_soup(url)
    list1 = soup.find(class_ = "album_soundlist").find_all('li')
    count = 1000
    for msg1 in list1:
        count = count  + 1
        id = msg1.get('sound_id')
        print id

        url ="http://www.ximalaya.com/tracks/"+id+".ext.text"
        mp3_url = get_mp3_url(url)
        save_mp3(mp3_url, count)

url = "http://www.ximalaya.com/54715628/album/4790468/"
url = "http://www.ximalaya.com/96295838/album/12642897/"
url = "http://www.ximalaya.com/44255360/album/5021722/"
url = "http://www.ximalaya.com/44255360/album/5021722?page=2"
url = "http://www.ximalaya.com/29044178/album/11953680/"
url = "http://www.ximalaya.com/44190264/album/5088879/"
url = "http://www.ximalaya.com/44190264/album/5088879?page=2"
url = "http://www.ximalaya.com/44190264/album/5088879?page=3"
test(url)
















