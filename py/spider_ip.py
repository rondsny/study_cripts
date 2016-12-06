#encoding=utf8

# http://www.xicidaili.com/nn/1

import urllib2
import BeautifulSoup

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent


f = open("./ip.txt", "w")

for page in range(1, 11):
    print "Page => " + str(page)
    url = 'http://www.xicidaili.com/nn/' + str(page)
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup.BeautifulSoup(res)
    ips = soup.findAll('tr')
    if len(ips) <= 0:
        print "Stop Page => " + str(page)
        break

    for x in range(1, len(ips)):
        ip = ips[x]
        tds = ip.findAll('td')
        ip_tmp = tds[1].string+"\t"+tds[2].contents[0]+"\n"
        print  ip_tmp
        f.write(ip_tmp)
    print "End Page => " + str(page)
