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
fd_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1664420006859.yml"
fd_L_yml = "/home/frank/.config/clash/profiles/1678421125458.yml"



class GetClashCf:
    def __init__(self,fs_W_yml,fs_L_yml,fd_W_yml,fd_L_yml):
        self.os_type = platform.system()
        if self.os_type == "Windows":
            self.fs_yml = fs_W_yml
            self.fd_yml = fd_W_yml
        if self.os_type == "Linux":
            self.fs_yml = fs_L_yml
            self.fd_yml = fd_L_yml
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}

    def getUrl(self):
        url_base = "https://www.cfmem.com/"
        req = requests.get(url_base,headers=self.headers)
        html = req.text
        text_find = etree.HTML(html)
        cur_url = text_find.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a/@href')[0]
        print(cur_url)
        next_req = requests.get(cur_url)
        html = next_req.text
        text_find = etree.HTML(html)
        durl = text_find.xpath('//*[@id="post-body"]/div[6]/span/span/div[2]/span/text()')[0]
        durl = durl.split("：")[1]
        #durl = re.search('https://.*\.yaml',html)
        print(durl)
        return durl

    def getYml(self):
        requests.packages.urllib3.disable_warnings()
        url = self.getUrl()
        req = requests.get(url,verify=False,headers=self.headers).text
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
        file = open(self.fd_yml,'w',encoding='UTF-8')
        for i in lineList:
            file.write(i)
        file.close()
            
    def get_yml_date(self):
        cur_date = str(datetime.date.today())
        if os.path.isfile(dir):
            filemt = time.localtime(os.stat(dir).st_mtime)
            filemt = time.strftime("%Y-%m-%d", filemt)
            if filemt == cur_date:
                return True
            else:
                return False
        return False

def main():
    get_cf = GetClashCf(fs_W_yml,fs_L_yml,fd_W_yml,fd_L_yml)
    # get_cf.getUrl()
    get_cf.getYml()
    get_cf.filterYml()
    print("clash yml file update success!")
    
if __name__ == "__main__":
    main()
