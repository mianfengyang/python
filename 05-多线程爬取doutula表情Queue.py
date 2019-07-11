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

class Producer(threading.Thread):

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='col-xs-6 col-sm-3']/img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')
            alt = img.get('alt')
            alt = re.sub(r'[，,!！\?？\*。]', '', alt)
            suffix = os.path.splitext(img_url)[1]
            filename = alt + suffix
            self.img_queue.put((img_url,filename))


class Consumer(threading.Thread):

    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()
            request.urlretrieve(img_url,'images/' + filename)



def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1,100):
        url = 'https://www.doutula.com/article/list/?page=%d' % x
        page_queue.put(url)

    for i in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    for i in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()

if __name__ == '__main__':
    main()