import re
import platform
import httpx
from fake_useragent import UserAgent
import datetime
import subprocess

fs_L_yml_frn = "/home/frank/.config/clash/freenode.yml"
fs_L_yml_verge_opr = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/opr.yaml"
fs_L_yml_verge_frn = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/frn.yaml"
fs_L_yml_opr = "/home/frank/.config/clash/openrunner.yml"
fs_W_yml = "D:\\project\\python\\learning\\spider\\frn_vpn\\frn.yml"
fd_L_yml_frn = "/home/frank/.config/clash/profiles/1722600464996.yml"
fd_L_yml_opr = "/home/frank/.config/clash/profiles/1721976735187.yml"
fd_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1693528527309.yml"

#downloadUrl = sys.argv[1]


class UpFreeNode:

    def __init__(self,fs_yml) -> None:
        self.fs_yml = fs_yml
        #self.fd_yml = fd_yml
        self.bigMon = ["01","05","07","08","10","12"]
        self.smallMon = ["04","06","09","11"]
        self.curYear = datetime.datetime.today().strftime('%Y')
        self.curMonth = datetime.datetime.today().strftime('%m')
        self.curDay = datetime.datetime.today().strftime('%d')
        self.day = int(self.curDay)
        if self.day < 10:
            self.day = '0' + str(self.day)
        else:
            self.day = str(self.day)
        self.baseUrl = "https://www.freeclashnode.com/uploads/"
        self.backUrl = self.curYear + '/' + self.curMonth + '/' + '3-' + self.curYear + self.curMonth + self.curDay + '.yaml'
        self.targetdir = "/data/project/cfvpn/"
        self.sourcedir = "/home/frank/.local/share/io.github.clash-verge-rev.clash-verge-rev/"
        self.sfile = "frn.yaml"
        

    def getDownloadUrl(self):
        self.ua = UserAgent()
        self.headers = {'User-Agent':self.ua.random}
        self.proxies = {'http://': 'http://127.0.0.1:7899'}
        self.downloadUrl = self.baseUrl + self.backUrl
        self.req = httpx.get(self.downloadUrl,headers=self.headers,verify=False)
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
            self.backUrl = self.curYear + '/' + self.curMonth + '/' + '3-' + self.curYear + self.curMonth + self.day + '.yaml'
            self.downloadUrl = self.baseUrl + self.backUrl
        else:
            self.downloadUrl = self.downloadUrl
        return self.downloadUrl
    
    def getYamlByRequests(self):
        self.downloadUrl = self.getDownloadUrl()
        req = httpx.get(self.downloadUrl,verify=False,headers=self.headers)
        req.encoding = 'utf-8'
        req = req.text
        with open(self.fs_yml,"w",encoding="utf-8") as file:
            file.write(req)

    def pushFileTogithub(self):
        copy = subprocess.run(['cp', self.sourcedir + self.sfile,self.targetdir], capture_output=True, text=True)
        print(copy.stdout)
        gitadd = subprocess.run(['git', 'add', self.sfile], capture_output=True, text=True)
        print(gitadd.stdout)
        comit = "update " + self.sfile + ' ' + datetime.datetime.today().strftime("%Y-%m-%d")
        gitcomit = subprocess.run(['git', 'commit', '-m',comit], capture_output=True, text=True)
        print(gitcomit.stdout)
        gitpush = subprocess.run(['git', 'push'], capture_output=True, text=True)
        print(gitpush.stdout)

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

class UpOpenrunner(UpFreeNode):
    def __init__(self, fs_yml) -> None:
        super().__init__(fs_yml)
        self.baseUrl = "https://freenode.openrunner.net/uploads/"
        self.backUrl = self.curYear + self.curMonth + self.curDay + '-clash.yaml'
        self.sfile = "opr.yaml"

if __name__ == "__main__":
    if platform.system() == "Linux":
        frn = UpFreeNode(fs_L_yml_verge_frn)
        opr = UpOpenrunner(fs_L_yml_verge_opr)
    if platform.system() == "Windows":
        frn = UpFreeNode(fs_W_yml,fd_W_yml) 
    frn.getYamlByRequests()
    frn.pushFileTogithub()
    #frn.filterYml()
    print("update success! " + frn.downloadUrl)
    opr.getYamlByRequests()
    opr.pushFileTogithub()
    #opr.filterYml()
    print("update success! " + opr.downloadUrl)
