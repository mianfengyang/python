from genericpath import isfile
import re
import os
import time
import datetime
import platform

from lxml import etree
import requests

dir_L_txt = "/home/frank/.config/clash/clash_subscribe_url.txt"
dir_W_txt = "D:\\project\\python\\learning\\spider\\changfen_vpn\\clash_subscribe_url.txt"
dir_L_yml = "/home/frank/.config/clash/changfen.yml"
dir_W_yml = "D:\\project\\python\\learning\\spider\\changfen_vpn\\changfen.yml"
dir_target_W_yml = "C:\\Users\\frank\\.config\\clash\\profiles\\1664420006859.yml"
dir_target_L_yml = "/home/frank/.config/clash/profiles/1665195083683.yml"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}

def get_os_type():
    return platform.system()
     

def save_url_txt_and_yml(os_type,url,dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml):
    if os_type == "Windows":
        dir_txt = dir_W_txt
        dir_yml = dir_W_yml
    if os_type == "Linux":
        dir_txt = dir_L_txt
        dir_yml = dir_L_yml
    matchPattern_url = re.compile(url)
    file = open(dir_txt,"a")
    while 1:
        line = file.readline()
        if not line:
            break
        elif matchPattern_url.search(line):
            pass
        else:
            file.write(str(datetime.date.today()) + "\t" + url + "\n")
    file.close()
    requests.packages.urllib3.disable_warnings()
    req = requests.get(url,verify=False,headers=headers).text
    with open(dir_yml,"w",encoding="utf-8") as file:
        file.write(req)


def get_yml_to_file(dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml):
    url_base = "https://www.cfmem.com/"
    req = requests.get(url_base)
    html = req.text
    text_find = etree.HTML(html)
    cur_url = text_find.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a/@href')[0]
    print(cur_url)
    next_req = requests.get(cur_url)
    html = next_req.text
    text_find = etree.HTML(html)
    clash_url = text_find.xpath('//*[@id="post-body"]/div/span/span/div[2]/span/text()')[0]
    clash_url = re.split("：",clash_url)[-1]
    print(clash_url)
    os_type = get_os_type()
    save_url_txt_and_yml(os_type,clash_url,dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml)

def filter_yml(os_type,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml):
    lineList = []
    matchPattern_hk = re.compile(r'香港')
    matchPattern_dns = re.compile(r'119.29.29.29')
    if os_type == "Windows":
        dir_source_yml = dir_W_yml
        dir_target_yml = dir_target_W_yml
    if os_type == "Linux":
        dir_source_yml = dir_L_yml
        dir_target_yml = dir_target_L_yml
    file = open(dir_source_yml,"r",encoding='UTF-8')
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
    file = open(dir_target_yml,'w',encoding='UTF-8')
    for i in lineList:
        file.write(i)
    file.close()
        
def get_yml_date(os_type,dir_target_W_yml,dir_target_L_yml):
    if os_type == "Windows":
        dir = dir_target_W_yml
    if os_type == "Linux":
        dir = dir_target_L_yml
    cur_date = str(datetime.date.today())
    if os.path.isfile(dir):
        filemt = time.localtime(os.stat(dir).st_mtime)
        filemt = time.strftime("%Y-%m-%d", filemt)
        if filemt == cur_date:
            return True
        else:
            return False
    return False

def main(dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml):
    os_type = get_os_type()
    if get_yml_date(os_type,dir_target_W_yml,dir_target_L_yml):
        print("current clash File is taoday, not update!")
    else:
        get_yml_to_file(dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml)
        filter_yml(os_type,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml)
        print("clash yml file update success!")
    
if __name__ == "__main__":
    main(dir_W_txt,dir_L_txt,dir_W_yml,dir_L_yml,dir_target_W_yml,dir_target_L_yml)