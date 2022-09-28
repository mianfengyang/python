from genericpath import isfile
import re
import os
from socketserver import BaseRequestHandler
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from urllib.parse import unquote
import urllib.request

url_source = "https://www.h3c.com/cn/BizPortal/TrainingPartner/TeachingMaterial/TeachingMaterialCertification.aspx"
url_pre = "https://www.h3c.com/cn/BizPortal/TrainingPartner/TeachingMaterial/Encrypt/"
url_sub_pdf_name_list = ['构建H3C高性能园区网络_第1篇_园区网概述', '构建H3C高性能园区网络_第2篇_VLAN技术', '构建H3C高性能园区网络_第3篇_生成树协议', 
                        '构建H3C高性能园区网络_第4篇_高可靠性技术', '构建H3C高性能园区网络_第5篇_IP组播', '构建H3C高性能园区网络_第6篇_园区网安全技术', 
                        '构建H3C高性能园区网络_第7篇_园区网管理维护', 'H3C大规模网络路由技术_第1篇_大规模网络路由概述', 'H3C大规模网络路由技术_第2篇_路由基础', 
                        'H3C大规模网络路由技术_第3_篇_OSPF', 'H3C大规模网络路由技术_第4篇_IS-IS', 'H3C大规模网络路由技术_第5篇_控制IGP路由', 'H3C大规模网络路由技术_第6篇_BGP-4', 
                        'H3C大规模网络路由技术_第7篇_IPv6基础', '构建安全优化的广域网_第1篇_广域网安全和优化概述']
url_sub_pdf_urlcode_list = []
url_sub_tail = "-yps1573.pdf"
download_url = []
save_dir = "D:\\Software\\Documents\\network\\H3C\\H3CSE"
test_url = "https://www.h3c.com/cn/BizPortal/TrainingPartner/TeachingMaterial/ReadingMaterials.aspx?TeachingID=d7adf2135b364dea907795b98e27edd7"
def get_url_sub_pdf_urlcode(list):
    for pdf_name in list:
        url_sub_pdf_urlcode_list.append(quote(pdf_name))

def get_download_url(list):
    for url in list:
        download_url.append(url_pre + url + url_sub_tail)

def get_exsit_file(dir,file_list):
    file_list = os.listdir(dir)
    return file_list

def get_cookies():
    f = open("file/h3c-cookies.txt","r")
    cookies={}#初始化cookies字典变量
    for line in f.read().split(';'):   #按照字符：进行划分读取
        #其设置为1就会把字符串拆分成2份
        name,value=line.strip().split('=',1)
        cookies[name]=value  #为字典cookies添加内容
    return cookies

def download_pdf(dir,list):
    cookies = get_cookies()
    for url in list:
        filename = url + url_sub_tail
        down_url = url_pre + filename
        filepath = dir + '/' + filename
        req = requests.get(down_url,cookies=cookies)
        with open(filepath, "wb") as code:
            code.write(req.content)

def test(dir,url1,url2):
    cookies = get_cookies()    
    # print(cookies)
    # filename = "第1篇_计算机网络基础" + url_sub_tail
    # filepath = dir + '/' + filename 
    # req1 = requests.get(url1,cookies=cookies)
    # req2 = requests.get(url2,cookies=cookies)
    # # with open(filepath, "wb") as code:
    # #     code.write(req2.content)
    # urllib.request.urlretrieve(url2,filepath)
    req = requests.get(url1,cookies=cookies).text
    print(req)




if __name__ == "__main__":
    # get_url_sub_pdf_urlcode(url_sub_pdf_name_list)
    # get_download_url(url_sub_pdf_name_list)
    # print(download_url)
    download_pdf(save_dir,url_sub_pdf_name_list)
    # url2 = url_pre + quote("第1篇_计算机网络基础") + url_sub_tail
    # test(save_dir, url_source, url2)
