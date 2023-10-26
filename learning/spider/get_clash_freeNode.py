import requests
from bs4 import BeautifulSoup
from datetime import date
import re


def get_clash_subscription():
    url = "https://clashfree.eu.org/freenode"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 查找包含当天日期的链接
    current_date = date.today().strftime("%m月%d日")
    #print(current_date)
    link_elements = soup.find_all("a", string=re.compile(current_date))
    #print(link_elements[0])
    
    link_url = link_elements[0].get("href")
    #print(link_url)
    link_response = requests.get(link_url)
    link_soup = BeautifulSoup(link_response.text, "html.parser")
    
    # 在链接所在的页面中查找包含以.yml结尾的文本
    span_elements = link_soup.find_all("p", string=re.compile('yml'))
    #print(span_elements)
    if span_elements:
        return span_elements[0].text
    
    return None

def download_subscribe(clash_s_url):
    r = requests.get(clash_s_url,stream=True)
    with open("/home/frank/project/clash/" + clash_s_url.split("/")[-1],"wb") as f:
        for data in r.iter_content(chunk_size=512):
            f.write(data)

clash_subscription_url = get_clash_subscription()
if clash_subscription_url:
    print("当天的Clash订阅文本：", clash_subscription_url)
    download_subscribe(clash_subscription_url)
else:
    print("当天的Clash订阅文本未找到")
