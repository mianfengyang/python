import re
import os
import platform
import requests
from fake_useragent import UserAgent
import datetime


fs_L_yml = "/home/frank/.config/clash/freenode.yml"
fs_W_yml = "D:\\project\\python\\learning\\spider\\frn_vpn\\frn.yml"
fd_L_yml = "/home/frank/.config/clash/profiles/1692090343227.yml"
fd_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1693528527309.yml"

#downloadUrl = sys.argv[1]


class UpFreeNode:

    def __init__(self,fs_L_yml,fs_W_yml,fd_L_yml,fd_W_yml) -> None:
        self.ostype = platform.system()
        if self.ostype == "Windows":
            self.fs_yml = fs_W_yml
            self.fd_yml = fd_W_yml
        if self.ostype == "Linux":
            self.fs_yml = fs_L_yml
            self.fd_yml = fd_L_yml
        self.bigMon = ["01","05","07","08","10","12"]
        self.smallMon = ["04","06","09","11"]
        self.curYear = datetime.datetime.today().strftime('%Y')
        self.curMonth = datetime.datetime.today().strftime('%m')
        self.curDay = datetime.datetime.today().strftime('%d')
        self.day = int(self.curDay)
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}
        self.proxies = {'http': 'http://127.0.0.1:7899'}
        if self.day < 10:
            self.day = '0' + str(self.day)
        else:
            self.day = str(self.day)
        self.baseUrl = "https://freenode.me/wp-content/uploads/"
        self.downloadUrl = self.baseUrl + self.curYear + '/' + self.curMonth + '/' + self.curMonth + self.curDay + '.yaml'
        self.req = requests.get(self.downloadUrl)
        print("Curday url is " + str(self.req.status_code))
        if self.req.status_code != 200:
            if self.curMonth in self.bigMon and self.curDay == "01":
                self.day = "30"
            if self.curMonth in self.smallMon and self.curDay == "01":
                self.day = "31"
            if self.curMonth == "03" and int(self.curYear) % 4 == 0 and self.curDay == "01":
                self.day = "29"
            else:
                self.day == "28"
            if int(self.curMonth) < 10 and self.curDay == "01":
                self.curMonth = "0" + str(int(self.curMonth) - 1)
            else:
                self.curMonth = self.curMonth
            if int(self.curDay) <= 10:
                self.day = "0" + str(int(self.curDay) - 1)
            else:
                self.day = str(int(self.curDay) - 1)
            self.downloadUrl = self.baseUrl + self.curYear + '/' + self.curMonth + '/' + self.curMonth + self.day + '.yaml'
        else:
            self.downloadUrl = self.downloadUrl


    def getYamlByRequests(self):
        requests.packages.urllib3.disable_warnings()
        req = requests.get(self.downloadUrl,verify=False,headers=self.headers,proxies=self.proxies)
        req.encoding = 'utf-8'
        req = req.text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(req)

    def preFilterYmlBysh(self):
        os.system('/home/frank/project/shell/python/prefilterfrn.sh')

    def filterYml(self):
        lineList = []
        rmnodeline = []
        matchPattern_filters = re.compile(r'香港|台湾|HK|中国|CN|JP|日本|法国|新加坡|德国')
        matchPattern_chacha20 = re.compile(r'chacha20')
        matchPattern_dns = re.compile(r'119.29.29.29')
        file = open(self.fs_yml,"r",encoding='UTF-8')
        while 1:
            line = file.readline()
            if not line:
                break
            elif matchPattern_filters.search(line):
                pass
            elif matchPattern_chacha20.search(line):
                rmnodeline.append("-" + line.split("{")[1].split("}")[0].split(",")[0].split(":")[1])
            elif matchPattern_dns.search(line):
                lineList.append(line.replace("119.29.29.29","218.2.135.1"))
            else:
                lineList.append(line)
        file.close()
        file = open(self.fd_yml,'w',encoding='UTF-8')
        for i in lineList:
            if i.strip() not in rmnodeline:
                file.write(i)
        file.close()


if __name__ == "__main__":
    frn = UpFreeNode(fs_L_yml,fs_W_yml,fd_L_yml,fd_W_yml)
    #frn.getYamlByWget()
    frn.getYamlByRequests()
    #frn.preFilterYml()
    frn.filterYml()
    print("update success! " + frn.downloadUrl)
