from genericpath import isfile
import re
import os
import subprocess
import time
import datetime
import platform
from lxml import etree
import requests
from fake_useragent import UserAgent


fs_L_yml = "/home/frank/.config/clash/changfen.yaml"
fs_L_yml_verge = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/cf.yaml"
fs_W_yml = "D:\\project\\python\\learning\\spider\\changfen_vpn\\changfen.yaml"
ft_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1664420006859.yaml"
ft_L_yml = "/home/frank/.config/clash/profiles/1723104912814.yml"
ft_L_yml_verge = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/cf.yaml"

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
        self.sourcedir = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/"
        self.sfile = "cf.yaml"
        self.sourcefile = self.sourcedir + self.sfile
        self.targetdir = "/data/project/cfvpn/"

    def downloadYmlByRequests(self):
        req = requests.get(self.base_url,headers=self.headers,proxies=self.proxies)
        html = req.text
        text_find = etree.HTML(html)
        cur_url = text_find.xpath('(//h2/a[contains(@title,"2024")])[1]/@href')[0]
        print(cur_url)
        next_req = requests.get(cur_url)
        html = next_req.text
        text_find = etree.HTML(html)
        #print(text_find.text())
        clash_url = text_find.xpath('(//span[contains(.,"mihomo")])[1]/text()')[0]
        print(clash_url)
        clash_url = re.split(">",clash_url)[-1].lstrip()
        #matchurl = re.search('https.*\.yaml',html).group()
        print(clash_url)
        requests.packages.urllib3.disable_warnings()
        req = requests.get(clash_url,headers=self.headers,proxies=self.proxies).text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(req)

    def filterYml(self):
        lineList = []
        rmNode = []
        matchPattern_hk = re.compile(r'香港|台湾|HK|中国|CN')
        matchPattern_dns = re.compile(r'119.29.29.29')
        matchPattern_chacha20 = re.compile(r'chacha20')
        file = open(self.fs_yml,"r",encoding='UTF-8')
        while 1:
            line = file.readline()
            if not line:
                break
            elif matchPattern_hk.search(line):
                pass
            elif matchPattern_chacha20.search(line):
                rmNode.append("-" + line.replace("-","").split(",")[0].split(":")[1])
                #print(rmNode)
            elif matchPattern_dns.search(line):
                lineList.append(line.replace("119.29.29.29","218.2.135.1"))
            else:
                lineList.append(line)
        file.close()
        file = open(self.ft_yml,'w',encoding='UTF-8')
        for i in lineList:
            if i not in rmNode:
                file.write(i)
        file.close()
            
    def pushFileTogithub(self):
        copy = subprocess.run(['cp', self.sourcefile,self.targetdir],text=True,capture_output=True)
        if not copy.returncode:
            print("copy file success")
        os.chdir(self.targetdir)
        gitadd = subprocess.run(['git', 'add', self.sfile],text=True,capture_output=True)
        if not gitadd.returncode:
            print(f"git add {self.sfile}")
        comit = "update " + self.sfile + ' ' + datetime.datetime.today().strftime("%Y-%m-%d")
        gitcomit = subprocess.run(['git', 'commit', '-m',comit],text=True,capture_output=True)
        if not gitcomit.returncode:
            print("git comit success")
        gitpush = subprocess.run(['git', 'push'],text=True,capture_output=True)
        if not gitpush.returncode:
            print("git push success")

    def isUp(self):
        cur_date = str(datetime.date.today())
        if os.path.isfile(self.ft_yml):
            filemt = time.localtime(os.stat(self.fs_yml).st_mtime)
            filemt = time.strftime("%Y-%m-%d", filemt)
            if filemt == cur_date:
                return True
            else:
                return False
        return False

def main():
    upcf = Upcf(fs_L_yml_verge,fs_W_yml,ft_L_yml_verge,ft_W_yml)
    upcf.downloadYmlByRequests()
    #upcf.filterYml()
    upcf.pushFileTogithub()
    ifup = upcf.isUp()
    if ifup:
        print("clash yml file update success!")
    else:
        print("clash yml file update error!")
    
if __name__ == "__main__":
    main()
