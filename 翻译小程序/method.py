# -*- coding: UTF-8 -*-
# 深入分析关于有道翻译的方法
import time
import random
import hashlib


# 有道方法---------------------------------
def generate_encryption_parameters(msg):
    # 翻译的文字
    data = generate_salt()
    # 生成的salt值
    i = data[1]
    # 当时时间
    now_time = data[0]
    # 生成md5值
    m = hashlib.md5()
    s = ("fanyideskweb" + msg + i + "Ygy_4c=r#e#4EX^NUGUc5")
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
