from genericpath import isfile
import re
import os
import time
import datetime
import platform

from lxml import etree
import requests
from fake_useragent import UserAgent
import socket
import socks
from retry import retry

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7899)
socket.socket = socks.socksocket

fs_L_yml = "/home/frank/.config/clash/changfen.yml"
fs_W_yml = "D:\\project\\python\\learning\\spider\\changfen_vpn\\changfen.yml"
ft_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1664420006859.yml"
ft_L_yml = "/home/frank/.config/clash/profiles/1678421125458.yml"

class Upcf():
    def __init__(self,fs_L_yml,fs_W_yml,ft_L_yml,ft_W_yml) -> None:
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}
        self.proxies = {'http': 'http://127.0.0.1:7899'}
        self.os_type = platform.system()
        self.base_url = "https://www.cfmem.com/"
        if self.os_type == "Windows":
            self.fs_yml = fs_W_yml
            self.ft_yml = ft_W_yml
        if self.os_type == "Linux":
            self.fs_yml = fs_L_yml
            self.ft_yml = ft_L_yml

    def downloadYmlByRequests(self):
        req = requests.get(self.base_url,headers=self.headers,proxies=self.proxies)
        html = req.text
        text_find = etree.HTML(html)
        cur_url = text_find.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a/@href')[0]
        print(cur_url)
        next_req = requests.get(cur_url)
        html = next_req.text
        text_find = etree.HTML(html)
        #print(text_find.text())
        clash_url = text_find.xpath('//*[@id="post-body"]/div[6]/span/span/div[3]/span/text()')[0]
        #print(clash_url)
        clash_url = re.split("：",clash_url)[-1]
        #matchurl = re.search('https.*\.yaml',html).group()
        print(clash_url)
        requests.packages.urllib3.disable_warnings()
        req = requests.get(clash_url,verify=False,headers=self.headers,proxies=self.proxies).text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(req)

    def filterYml(self):
        lineList = []
        matchPattern_hk = re.compile(r'香港|台湾|HK|中国|CN')
        matchPattern_dns = re.compile(r'119.29.29.29')
        file = open(self.fs_yml,"r",encoding='UTF-8')
        while 1:
            line = file.readline()
            if not line:
                break
            elif matchPattern_hk.search(line):
                pass
            elif matchPattern_dns.search(line):
                lineList.append(line.replace("119.29.29.29","218.2.135.1"))
            else:
                lineList.append(line)
        file.close()
        file = open(self.ft_yml,'w',encoding='UTF-8')
        for i in lineList:
            file.write(i)
        file.close()
            
    def isUp(self):
        cur_date = str(datetime.date.today())
        if os.path.isfile(self.ft_yml):
            filemt = time.localtime(os.stat(self.ft_yml).st_mtime)
            filemt = time.strftime("%Y-%m-%d", filemt)
            if filemt == cur_date:
                return True
            else:
                return False
        return False

def main():
    upcf = Upcf(fs_L_yml,fs_W_yml,ft_L_yml,ft_W_yml)
    upcf.downloadYmlByRequests()
    upcf.filterYml()
    ifup = upcf.isUp()
    if ifup:
        print("clash yml file update success!")
    else:
        print("clash yml file update error!")
    
if __name__ == "__main__":
    main()
