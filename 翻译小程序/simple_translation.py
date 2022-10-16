# -*- coding: UTF-8 -*-

# 此文件为有道无反爬获取翻译
import requests
from utils import Headers
import random
import time

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://fanyi.youdao.com/",
    "User-Agent": Headers.Header_forge_chrome[random.randint(1, len(Headers.Header_forge_chrome))]
}
response = requests.get('https://fanyi.youdao.com/', headers=headers)
cookie = ""
# 获取有道翻译cookie
for item in response.cookies.items():
    if "OUTFOX_SEARCH_USER_ID" in item:
        cookie += str(item[0]) + ":" + str(item[1])
Now = int(time.time() * 1000)
youdao_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": cookie,
    "Host": "fanyi.youdao.com",
    "Referer": "https://fanyi.youdao.com/",
    "User-Agent": Headers.Header_forge_chrome[random.randint(1, len(Headers.Header_forge_chrome))]
}
param = {
    "i": "test",
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "doctype": "json",
    "version": 2.1,
    "keyfrom": "fanyi.web",
    "action": "FY_BY_REALTlME"
}
response = requests.post('https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule', data=param,
                         headers=youdao_headers)
print(response.json()['translateResult'][0][0]['tgt'])
