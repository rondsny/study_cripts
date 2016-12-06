#encoding=utf8

import sys
import urllib
import urllib2
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def pares(html):
    soup = BeautifulSoup(html, "html.parser")
    account = len(soup.find_all("h4", ""))
    name_list = []
    for i in range(account):
        name = soup.find_all("h4", "")[i].find_all("a")[2].string
        print name
        send(name, "卡巴超中午好啊")
        name_list.append(name)
    return name_list

def getCommentsHtml(index):
    url = "http://www.cnblogs.com/mvc/blog/GetComments.aspx"
    params = {
        "postId": "6095149",
        "blogApp": "rond",
        "pageIndex": `index`,
        "anchorCommentId": `0`,
        "_": "1480495756000"
    }

    url_params = urllib.urlencode(params)
    res = urllib2.urlopen(url, data=url_params).read()
    return json.loads(res)['commentsHtml']

def send(name, cont):
    url = "https://msg.cnblogs.com/ajax/msg/send"
    header = {
        "Cookie": ""
    }
    params = {
        "incept": name,
        "title": "spider script test",
        "content": `cont`
    }
    print params
    url_params = urllib.urlencode(params)
    request = urllib2.Request(url, headers=header, data=url_params)
    print urllib2.urlopen(request).read()

i = 1
while True:
    html = getCommentsHtml(i)
    if(html.count(u"comment_date") < 1):
        print "Over: " + `i`
        break
    else:
        print "GetPage: " + `i`
        # print html
        print pares(html)
    i = i + 1

