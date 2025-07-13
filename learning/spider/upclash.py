import re

import platform
import datetime
import requests

from fake_useragent import UserAgent
from lxml import etree
from threading import Thread


class UpFreeNode:

    def __init__(self,fs_yml) -> None:
        self.fs_yml = fs_yml
        self.curYear = datetime.datetime.today().strftime('%Y')
        self.curMonth = datetime.datetime.today().strftime('%m')
        self.curDay = datetime.datetime.today().strftime('%d')
        self.baseUrl = "https://node.freeclashnode.com/uploads/"
        self.backUrl = self.curYear + '/' + self.curMonth + '/' + '3-' + self.curYear + self.curMonth + self.curDay + '.yaml'
        self.downloadUrl = None
        
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}
        self.proxies = {
                        "http": "http://127.0.0.1:7899",
                        "https": "http://127.0.0.1:7899"
                        }



    def getDownloadUrl(self):
        self.bigMon = ["01","05","07","08","10","12"]
        self.smallMon = ["04","06","09","11"]
        self.day = int(self.curDay)
        if self.day < 10:
            self.day = '0' + str(self.day)
        else:
            self.day = str(self.day)
        self.downloadUrl = self.baseUrl + self.backUrl
        self.req = requests.get(url=self.downloadUrl,headers=self.headers,verify=False)
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
            self.backUrl = self.curYear + '/' + self.curMonth + '/' + '3-' + self.curYear + self.curMonth + self.day + '.yaml'
            self.downloadUrl = self.baseUrl + self.backUrl
        else:
            self.downloadUrl = self.downloadUrl
        return self.downloadUrl
    
    def getYamlByRequests(self):
        self.downloadUrl = self.getDownloadUrl()
        if "yaml" not in self.downloadUrl:
            print("Get download url failed")
            return
        print(f"DownloadUrl is {self.downloadUrl}")
        self.req = requests.get(url=self.downloadUrl,headers=self.headers,verify=False,timeout=None)
        self.req.encoding = 'utf-8'
        self.req_text = self.req.text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(self.req_text)
        print(f"Write file {self.fs_yml} success")

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


class UpChangfen(UpFreeNode):
    def __init__(self, fs_yml) -> None:
        super().__init__(fs_yml)
        self.baseUrl = "https://www.cfmem.com"

    def getDownloadUrl(self):
        self.req = requests.get(url=self.baseUrl,headers=self.headers,verify=False,timeout=None)
        if self.req.status_code != 200:
            print(f"Get url failed, status code is {self.req.status_code}")
            return

        self.html = self.req.text
        self.text_find = etree.HTML(self.html)
        self.cur_url = self.text_find.xpath('(//h2/a/@href)[1]')[0]
        #print(self.cur_url)
        self.next_req = requests.get(url=self.cur_url,headers=self.headers,verify=False,timeout=None)
        if self.next_req.status_code != 200:
            print(f"Get url failed, status code is {self.next_req.status_code}")
            return
        self.html = self.next_req.text
        self.text_find = etree.HTML(self.html)
        #print(text_find.text())
        self.downloadUrl = self.text_find.xpath('//span[contains(.,"mihomo")]/text()')[0]
        self.downloadUrl = re.split(">",self.downloadUrl)[-1].lstrip()
        #print(self.downloadUrl)
        return self.downloadUrl


def upcf(fs):
    cf = UpChangfen(fs)
    cf.run()
    
def upfrn(fs):
    frn = UpFreeNode(fs)
    frn.run()


if __name__ == "__main__":
    fs_L_verge_frn = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/profiles/LioKZoEucV3P.yaml"
    fs_L_verge_cf = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/profiles/LNxSTKecI7wq.yaml"
    fs_W_verge_cf = "C:\\Users\\frandon\\AppData\\Roaming\\io.github.clash-verge-rev.clash-verge-rev\\profiles\\LpjWCKEUn4PN.yaml"
    fs_W_verge_frn = "C:\\Users\\frandon\\AppData\\Roaming\\io.github.clash-verge-rev.clash-verge-rev\\profiles\\Lva8saf6iNxY.yaml"

    
    if platform.system() == "Linux":
        tfrn = Thread(target=upfrn,args=(fs_L_verge_frn,))
        tcf = Thread(target=upcf,args=(fs_L_verge_cf,))
        tfrn.start()
        tfrn.join()
        tcf.start()
        tcf.join()
    if platform.system() == "Windows":
        tfrn = Thread(target=upfrn,args=(fs_W_verge_frn,))
        tcf = Thread(target=upcf,args=(fs_W_verge_cf,))
        tfrn.start()
        tfrn.join()
        tcf.start()
        tcf.join()