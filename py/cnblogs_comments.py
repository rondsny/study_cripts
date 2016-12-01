#encoding=utf8

import sys
import urllib
import urllib2
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

uuid = ""
blogApp = ""
cookie = ""

# 按页获取评论html内容
def getCommentsHtml(postId, index):
    url = "http://www.cnblogs.com/mvc/blog/GetComments.aspx"
    global blogApp
    params = {
        "postId": `postId`,
        "blogApp": blogApp,
        "pageIndex": `index`,
        "anchorCommentId": `0`,
        "_": "0"
    }

    url_params = urllib.urlencode(params)
    res = urllib2.urlopen(url, data=url_params).read()
    return json.loads(res)['commentsHtml']

# 提取评论数据
def pares(html):
    soup = BeautifulSoup(html, "html.parser")
    account = len(soup.find_all("h4", ""))
    temp_list = []
    parent_list = []
    for i in range(account):
        temp = soup.find_all("h4", "")[i]
        cont_as = soup.find_all("p", "")[i].find_all("a")

        pcId = temp.find_all("a")[1]["name"]
        name = temp.find_all("a")[2].string

        if cont_as[0].string == "@":
            parentId = cont_as[0]['href'][1:]
            dic = {
                "pcId": pcId,
                "parentId": parentId,
                "name": name
            }
            parent_list.append(dic)
        else:
            dic = {
                "pcId": pcId,
                "name": name
            }
            temp_list.append(dic)
    return temp_list, parent_list

# 过滤掉已经回复了的评论
def filter_list(s_list, p_list, author):
    for p in p_list:
        if p['name'] == author:
            for s in s_list:
                if s['pcId'] == p['parentId']:
                    s_list.remove(s)
    return s_list

# 回复评论
def reply(postId, pcId, cont):
    global blogApp,cookie
    url = "http://www.cnblogs.com/mvc/PostComment/Add.aspx"
    header = {
        "Cookie": cookie
    }
    params = {
        "blogApp": blogApp,
        "body": cont,
        "parentCommentId": pcId,
        "postId": postId
    }
    print params
    url_params = urllib.urlencode(params)
    print url_params
    request = urllib2.Request(url, headers=header, data=url_params)
    print urllib2.urlopen(request).read()

# 逻辑
def loop_post(postId):
    i = 1
    author = "Ron Ngai"
    s_list = []
    p_list = []
    while True:
        html = getCommentsHtml(postId, i)
        if(html.count(u"comment_date") < 1):
            print "Over Page: " + `i`
            break
        else:
            print "Current Page: " + `i`
            # print html
            s_t_list, p_t_list = pares(html)
            s_list += s_t_list
            p_list += p_t_list
        i = i + 1

    s_list = filter_list(s_list, p_list, author)
    print s_list

    for i in range(0, len(s_list)):
        pcId = s_list[i]['pcId']
        name = s_list[i]['name']
        cont = "@" + name + u"\n 感谢评论或建议 —— 这是一条自动回复（如有打搅，还望海涵）"
        reply(postId, pcId, cont)
        print "reply: " + pcId + " - " + name

# -------------------------

url = "http://feed.cnblogs.com/blog/u/"+ uuid + "/rss"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")

notes = soup.find_all('entry')
for note in notes:
    str = note.id.string
    postId = str[30:-5]
    loop_post(int(postId))