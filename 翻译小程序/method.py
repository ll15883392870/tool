# -*- coding: UTF-8 -*-
# 深入分析关于有道翻译的方法
import time
import random
import hashlib
from pyquery import PyQuery

# 有道方法---------------------------------
import requests
import re


def get_encryption():
    response = requests.get("https://shared.ydstatic.com/fanyi/newweb/v1.1.10/scripts/newweb/fanyi.min.js")
    path = re.findall('sign: n.md5(.*)t.recordUpdate', response.text)
    data = str(path).split("\"")[3]
    return data


def generate_encryption_parameters(msg):
    # 翻译的文字
    data = generate_salt()
    # 加密参数
    encryption = get_encryption()
    # 生成的salt值
    i = data[1]
    # 当时时间
    now_time = data[0]
    # 生成md5值
    m = hashlib.md5()
    s = ("fanyideskweb" + msg + i + encryption)
    m.update(s.encode('utf-8'))
    # 返回salt,lts,bv值
    return i, now_time, m.hexdigest(),


# 生成salt参数
def generate_salt():
    # 现在的时间
    now_time = int(time.time() * 1000)
    # 随机数
    i = now_time + random.randint(0, 10)
    return str(now_time), str(i)


# 生成param中bv参数
def bv(data):
    try:
        browser = data.split("Mozilla/")[1]
    except Exception as e:
        browser = data.split("Opera/")[1]
    return hashlib.md5((browser).encode('utf-8')).hexdigest()

# 百度方法---------------------------------
