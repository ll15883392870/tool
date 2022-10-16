# -*- coding: UTF-8 -*-
# 此文件为有道反爬获取翻译
import random

import requests
from method import generate_encryption_parameters, bv
from utils import Headers


def get_youdao(msg):
    get_headers = Headers.Header_forge_chrome[random.randint(1, len(Headers.Header_forge_chrome))]
    cookie = ['OUTFOX_SEARCH_USER_ID=-1927650476@223.97.13.65;', 'OUTFOX_SEARCH_USER_ID=-2022895048@10.168.8.76;']
    encryption = generate_encryption_parameters(msg)
    youdao_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie[random.randint(0, len(cookie) - 1)],
        "Referer": "http://fanyi.youdao.com/",
        "Origin": "http://fanyi.youdao.com",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": get_headers
    }
    data = {
        "i": msg,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": encryption[0],
        "sign": encryption[2],
        "lts": encryption[1],
        "bv": bv(youdao_headers['User-Agent']),
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CL1CKBUTTON"

    }
    response = requests.post('http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule', data=data,
                             headers=youdao_headers).json()

    if "translateResult" in response:
        return response['translateResult'][0][0]['tgt']
    elif "errorCode" in response:
        print("请在源代码methods中修改加密参数")
        return "请联系开发人员进行更新!3539739077@qq.com"


def get_baidu(msg):
    get_headers = Headers.Header_forge_chrome[random.randint(1, len(Headers.Header_forge_chrome))]
    headers = {
        "User-Agent": get_headers,
        "Cookie": 'BIDUPSID=BDC449922D81F6A4E2C6D7F3575E7924; PSTM=1664101128; BAIDUID=0666A29C030897BBDEE57F650D3CC3BF:FG=1; MCITY=-74%3A; BAIDUID_BFESS=0666A29C030897BBDEE57F650D3CC3BF:FG=1; ZFY=1UFkkDTOYGc33oW6WFylMwFCVd5oUZLeTHrNGhdZEIU:C; RT="z=1&dm=baidu.com&si=0pbp5mhszox&ss=l98f1qgl&sl=6&tt=55o&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=14yw&ul=15exb&hd=15eyf"; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1665914049; ZD_ENTRY=bing; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1665932614; ab_sr=1.0.1_ZWU1NTIyMDNkNmY1NjdkYmM2ZjAxODkxODM3YzE0YzBhOWEyMjdiNmNmNWM3YzFlYjJmNTY1Y2VmZDk4NzgwZGZmMzUyYWZiOGM3YTc3NTYzNmJkZDU4MTliYmVhMWIyMTUwNGM4MmM2OTQyMTBjMTRkY2IzYWMxNjA2NDhkMTE4ZTUxZjEwNDEyZjNjNjk1N2NjMGM2NGM0ODQyYmI3Yw=='
    }
    base_url = 'https://fanyi.baidu.com/sug'
    data = {
        "kw": msg
    }
    response = requests.post(base_url, headers=headers, data=data).json()
    if "data" in response:
        return response['data'][0]['v']
    else:
        return "请联系开发人员进行更新!3539739077@qq.com"

