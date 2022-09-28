import re
import os

from lxml import etree
import requests

url_base = "https://www.cfmem.com/"
req = requests.get(url_base)
html = req.text
text_find = etree.HTML(html)
cur_url = text_find.xpath('//*[@id="Blog1"]/div[1]/article[1]/div[1]/h2/a/@href')[0]
next_req = requests.get(cur_url)
html = next_req.text
text_find = etree.HTML(html)
clash_url = text_find.xpath('//*[@id="post-body"]/div[7]/span/span/div[2]/span/text()')[0]
clash_url = re.split("：",clash_url)[-1]
print(clash_url)
f = open("clash_subscribe_url.txt","w")
f.write(clash_url)
f.close()
