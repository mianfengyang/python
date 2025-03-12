import re
import os
import subprocess
import platform
import datetime

import httpx
from fake_useragent import UserAgent
from lxml import etree
from threading import Thread


class UpFreeNode:

    def __init__(self,fs_yml) -> None:
        self.fs_yml = fs_yml
        #self.fd_yml = fd_yml
        self.curYear = datetime.datetime.today().strftime('%Y')
        self.curMonth = datetime.datetime.today().strftime('%m')
        self.curDay = datetime.datetime.today().strftime('%d')
        self.baseUrl = "https://www.freeclashnode.com/uploads/"
        self.backUrl = self.curYear + '/' + self.curMonth + '/' + '1-' + self.curYear + self.curMonth + self.curDay + '.yaml'
        self.downloadUrl = None
        self.targetdir = "/data/project/cfvpn/"
        self.sourcedir = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/"
        self.sfile = "frn.yaml"
        self.sourcefile = self.sourcedir + self.sfile
        
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}
        self.proxies = {'http://': 'http://127.0.0.1:7899','https://': 'http://127.0.0.1:7899'}

        os.chdir("/data/project/python/learning/spider")


    def getDownloadUrl(self):
        self.bigMon = ["01","05","07","08","10","12"]
        self.smallMon = ["04","06","09","11"]
        self.day = int(self.curDay)
        if self.day < 10:
            self.day = '0' + str(self.day)
        else:
            self.day = str(self.day)
        self.downloadUrl = self.baseUrl + self.backUrl
        self.req = httpx.get(self.downloadUrl,headers=self.headers,verify=False)
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
            self.backUrl = self.curYear + '/' + self.curMonth + '/' + '1-' + self.curYear + self.curMonth + self.day + '.yaml'
            self.downloadUrl = self.baseUrl + self.backUrl
        else:
            self.downloadUrl = self.downloadUrl
        return self.downloadUrl
    
    def getYamlByRequests(self):
        try:
            self.downloadUrl = self.getDownloadUrl()
        except Exception as e:
            print(f"can not get downloadUrl, {e}")
        else:
            print(f"DownloadUrl is {self.downloadUrl}")
            if "github" in self.downloadUrl:
                self.req = httpx.get(url=self.downloadUrl,headers=self.headers,proxies=self.proxies)
            else:
                self.req = httpx.get(self.downloadUrl,verify=False,headers=self.headers)
            self.req.encoding = 'utf-8'
            self.req = self.req.text
            with open(self.fs_yml,"w",encoding="utf-8") as file:
                file.write(self.req)
            print(f"Download success and wirte to file {self.sfile}")

    def gitAddCommit(self):
        copy = subprocess.run(['cp', self.sourcefile,self.targetdir],text=True,capture_output=True)
        if copy.returncode == 0:
            print(f"copy file {self.sfile} to {self.targetdir} success")
        os.chdir(self.targetdir)
        gitadd = subprocess.run(['git', 'add', self.sfile],text=True,capture_output=True)
        if gitadd.returncode == 0:
            print(f"git add {self.sfile}")
        comit = "update " + self.sfile + ' ' + datetime.datetime.today().strftime("%Y-%m-%d")
        gitcomit = subprocess.run(['git', 'commit', '-m',comit],text=True,capture_output=True)
        if gitcomit.returncode == 0:
            print(f"git comit {comit} success")

    def filterYml(self):
        lineList = []
        rmnodeline = []
        matchPattern_filters = re.compile(r'香港|台湾|中国')
        matchPattern_chacha20 = re.compile(r'chacha20')
        matchPattern_dns = re.compile(r'119.29.29.29')
        file = open(self.fs_yml,"r",encoding='UTF-8')
        while 1:
            line = file.readline()
            if not line:
                break
            elif matchPattern_filters.search(line):
                pass
                #print(line)
            elif matchPattern_chacha20.search(line):
                #print(line)
                #rmnodeline.append("-" + line.split(",")[0].split(":")[1])
                rmnodeline.append("-" + line.lstrip().replace("-","").split(",")[0].split(":")[1])
                print(rmnodeline)
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

    def run(self):
        print(f"=============================== Up {type(self).__name__} ===============================")
        self.getYamlByRequests()
        self.gitAddCommit()

class Upclashfans(UpFreeNode):
    def __init__(self, fs_yml) -> None:
        super().__init__(fs_yml)
        self.baseUrl = "https://www.freeclashnode.com/uploads/"
        self.backUrl = self.curYear + '/' + self.curMonth + '/3-' + self.curYear + self.curMonth + self.curDay + '.yaml'
        self.sfile = "cfs.yaml"
        self.sourcefile = self.sourcedir + self.sfile

class Upcgh(UpFreeNode):
    def __init__(self, fs_yml):
        super().__init__(fs_yml)
        self.baseUrl = "https://clashgithub.com/wp-content/uploads/rss/"
        self.backUrl = self.curYear + self.curMonth + self.curDay + '.yml'
        self.sfile = "cgh.yaml"
        self.sourcefile = self.sourcedir + self.sfile
        self.downloadUrl = self.baseUrl + self.backUrl

    def getDownloadUrl(self):
        return self.downloadUrl 

class UpChangfen(UpFreeNode):
    def __init__(self, fs_yml) -> None:
        super().__init__(fs_yml)
        self.baseUrl = "https://www.cfmem.com/"
        self.sfile = "cf.yaml"
        self.sourcefile = self.sourcedir + self.sfile
        self.testfile = "/data/project/python/learning/spider/cf.html"

    def getDownloadUrl(self):
        try:
            self.req = httpx.get(url=self.baseUrl,headers=self.headers,follow_redirects=True)
        except Exception as e:
            print(f"Query {self.baseUrl} failed {e}")
        self.html = self.req.text
        #print(self.html)
        with open(self.testfile,"w",encoding="utf-8") as cfhtml:
            cfhtml.write(self.html)
        self.text_find = etree.HTML(self.html)
        self.cur_url = self.text_find.xpath('(//h2/a//@href)[1]')[0]
        print(self.cur_url)
        self.next_req = httpx.get(self.cur_url)
        self.next_html = self.next_req.text
        self.text_find = etree.HTML(self.next_html)
        #print(self.text_find.text())
        self.downloadUrl = self.text_find.xpath('(//span[contains(.,"mihomo")])[1]/text()')[0]
        self.downloadUrl = re.split(">",self.downloadUrl)[-1].lstrip()
        return self.downloadUrl

def gitPush():
    os.chdir("/data/project/cfvpn")
    if subprocess.run(['git','push'],text=True,capture_output=True).returncode == 0:
        print("git push success")

def upcf(fs):
    cf = UpChangfen(fs)
    cf.run()
    
def upfrn(fs):
    frn = UpFreeNode(fs)
    frn.run()
    
def upcfs(fs):
    cfs = Upclashfans(fs)
    cfs.run()

def upcgh(fs):
    cgithub = Upcgh(fs)
    cgithub.run()

def upAll(ins,fs):
    t = ins(fs)
    t.run()


if __name__ == "__main__":
    fs_L_c4w_frn = "/home/frank/.config/clash/freenode.yaml"
    fs_L_c4w_opr = "/home/frank/.config/clash/openrunner.yaml"
    fs_L_c4w_cf = "/home/frank/.config/clash/changfen.yaml"
    fs_L_verge_cfs = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/cfs.yaml"
    fs_L_verge_frn = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/frn.yaml"
    fs_L_verge_cf = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/cf.yaml"
    fs_W_yml = "D:\\project\\python\\learning\\spider\\frn_vpn\\frn.yml"
    fd_L_c4w_frn = "/home/frank/.config/clash/profiles/1722600464996.yml"
    fd_L_c4w_opr = "/home/frank/.config/clash/profiles/1721976735187.yml"
    fd_L_c4w_opr = "/home/frank/.config/clash/profiles/1721976735187.yml"

    fd_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1693528527309.yml"
    
    if platform.system() == "Linux":
        tfrn = Thread(target=upfrn,args=(fs_L_verge_frn,))
        tcf = Thread(target=upcf,args=(fs_L_verge_cf,))
        tcfs = Thread(target=upcfs,args=(fs_L_verge_cfs,))
    if platform.system() == "Windows":
        frn = UpFreeNode(fs_W_yml) 
    tfrn.start()
    tfrn.join()
    tcf.start()
    tcf.join()
    tcfs.start()
    tcfs.join()
    gitPush()
    