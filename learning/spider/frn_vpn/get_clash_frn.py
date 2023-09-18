import re
import os
import sys
import platform
import requests
from fake_useragent import UserAgent
from retry import retry
import datetime


fs_L_yml = "/home/frank/.config/clash/freenode.yml"
fs_W_yml = "D:\\project\\python\\learning\\spider\\frn_vpn\\frn.yml"
fd_L_yml = "/home/frank/.config/clash/profiles/1692090343227.yml"
fd_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1693528527309.yml"

#downloadUrl = sys.argv[1]


class upFreeNode:

    def __init__(self,fs_L_yml,fs_W_yml,fd_L_yml,fd_W_yml) -> None:
        self.ostype = platform.system()
        if self.ostype == "Windows":
            self.fs_yml = fs_W_yml
            self.fd_yml = fd_W_yml
        if self.ostype == "Linux":
            self.fs_yml = fs_L_yml
            self.fd_yml = fd_L_yml


    def mergeDownloadUrl(self):
        self.curYear = datetime.datetime.today().strftime('%Y')
        self.curMonth = datetime.datetime.today().strftime('%m')
        self.curDay = datetime.datetime.today().strftime('%d')
        self.baseUrl = "https://freenode.me/wp-content/uploads/"
        self.downloadUrl = self.baseUrl + self.curYear + '/' + self.curMonth + '/' + self.curMonth + self.curDay + '.yaml'
        return self.downloadUrl


    def getYamlFromUrl(self):
        ua = UserAgent()
        headers = {'User-Agent':ua.random}
        proxies = {'http': 'http://127.0.0.1:7899'}
        requests.packages.urllib3.disable_warnings()
        req = requests.get(self.downloadUrl,verify=False,headers=headers,proxies=proxies)
        req.encoding = 'utf-8'
        req = req.text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(req)

    def preFilterYml(self):
        os.system('/home/frank/project/python/prefilterfrn.sh')

    def filterYml(self):
        lineList = []
        matchPattern_hk = re.compile(r'香港|台湾|HK|中国|CN|JP|日本')
        matchPattern_dns = re.compile(r'119.29.29.29')
        file = open(self.fs_yml,"r",encoding='UTF-8')
        while 1:
            line = file.readline()
            if not line:
                break
            elif matchPattern_hk.search(line):
                pass
            elif matchPattern_dns.search(line):
                lineList.append(line.replace("119.29.29.29","114.114.114.114"))
            else:
                lineList.append(line)
        file.close()
        file = open(self.fd_yml,'w',encoding='UTF-8')
        for i in lineList:
            file.write(i)
        file.close()


if __name__ == "__main__":
    frn = upFreeNode(fs_L_yml,fs_W_yml,fd_L_yml,fd_W_yml)
    frn.mergeDownloadUrl()
    frn.getYamlFromUrl()
    #frn.preFilterYml()
    frn.filterYml()
