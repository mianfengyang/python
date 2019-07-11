# coding=utf-8

"""
==============================================================
# @Time    : 2019/7/9 20:43
# @Author  : mifyang
# @Email   : mifyang@126.com
# @File    : 05-多线程爬取doutula表情Queue
# @Software: PyCharm
==============================================================
"""
from queue import Queue
import threading
import os
from lxml import etree
import requests
from urllib import request
import re

def parse_page(url):
    response = requests.get(url)
    text = response.text
    html = etree.HTML(text)
    imgs = html.xpath("//div[@class='col-xs-6 col-sm-3']/img[@class!='gif']")
    for img in imgs:
        img_url = img.get('data-original')
        alt = img.get('alt')
        alt = re.sub(r'[，,!！\?？]', '', alt)
        suffix = os.path.splitext(img_url)[1]
        filename = alt + suffix
        request.urlretrieve(img_url,'images/' + filename)
        #print(filename)

def main():
    for x in range(1,10):
        url = 'https://www.doutula.com/article/list/?page=%d' % x
        parse_page(url)

if __name__ == '__main__':
    main()