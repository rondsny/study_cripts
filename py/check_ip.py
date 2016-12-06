#encoding=utf8

import urllib
import socket

socket.setdefaulttimeout(1)
f = open("./ip.txt")
lines = f.readlines()
proxys = []
allow_proxys = []

for i in range(0, len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://" + ip[0] + ":" + ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)

url = "http://ip.chinaz.com/getip.aspx"

for proxy in proxys:
    try:
        res = urllib.urlopen(url, proxies=proxy).read()
        allow_proxys.append(proxy)
        print res
    except Exception,e:
        print proxy
        print e 
        continue

print "[ALLOW IPS]"

fsave = open("./ip_legal.txt", "w")
for proxy in allow_proxys:
    fsave.write(proxy["http"]+"\n")