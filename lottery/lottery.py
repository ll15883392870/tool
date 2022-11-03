# -*-coding: utf-8-*-

# 注：此代码仅供学习使用，若使用者造成网站瘫痪，开发人员不负法律责任

import re
import time

import requests
import random
from utils.Headers import Header_forge_chrome
from lxml import etree

arr = []
base_url = 'http://www.cwl.gov.cn/cwl_admin/ui/catalog/11305/pc/index_{num}.shtml'
max_page = 129
file = '中奖.txt'

ips = ['120.220.220.95:8085', '223.96.90.216:8085', '61.216.185.88:60808', '58.20.184.187:9091', '112.14.47.6:52024',
       '60.170.204.30:8060']

header_length = len(Header_forge_chrome)
ip_length = len(ips)

ip_num = random.randint(0, ip_length - 1)
proxy = {"https": ips[ip_num]}


def scrapy_index():
    for i in range(1, max_page):
        number = random.randint(0, header_length - 1)
        headers = {
            "User-Agent": Header_forge_chrome[number],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Host": "www.cwl.gov.cn"
        }

        url = base_url.format(num=str(i))
        response = requests.get(url, headers=headers, proxies=proxy)
        html = etree.HTML(response.text)
        every = html.xpath("//div[@class='body-content']//ul/a/@href")
        for i in every:
            print(i)
            scrapy_detail(str(i))
            time.sleep(2)


def scrapy_detail(url):
    number = random.randint(0, header_length - 1)
    headers = {
        "User-Agent": Header_forge_chrome[number],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host": "www.cwl.gov.cn"
    }
    response = requests.get(url, headers=headers, proxies=proxy)
    first = re.findall("khHq =(.*?)</script>", response.text, re.S)
    second = re.compile("\d{2}")
    result = re.findall(second, str(first))
    with open(file, 'a+', encoding='utf-8') as f:
        f.write(str(result) + '\n')


if __name__ == '__main__':
    scrapy_index()
    print('完成')
