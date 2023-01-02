import os.path

import requests
from lxml import etree
from typing import *


DATA_DIR = "./data"
BASE_URL = "https://live.douyin.com/hot_live"
NEXT_PAGE_URL = "https://live.douyin.com/webcast/web/partition/detail/room/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 " \
             "Safari/537.36 "


def get_index_page_html() -> str:
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    index_html = DATA_DIR + os.sep + "index.html"
    if not os.path.exists(index_html):
        save_index_page(index_html)

    with open(index_html, mode='r+', encoding='utf-8')as f:
        return f.read()


def get_request_header() -> Dict:
    return {
        'user-agent': USER_AGENT,
        'accept-language': "zh-CN,zh;q=0.9",
        'content - type': 'application/json;charset=UTF-8',
    }


def save_index_page(file: str):
    resp = requests.get(BASE_URL, headers=get_request_header())

    with open(file, mode='w+', encoding='utf-8')as f:
        f.write(resp.text)


def get_index_page_hot_lives():
    html_str = get_index_page_html()
    html = etree.HTML(html_str)
    live_list = html.xpath("/html/body/div[1]/div/main/div[3]/div/div[2]/div/ul/li")
    for live in live_list:
        live_url = live.xpath("a/@href")[0]
        live_id = live_url.split("/")[-1]
        live_name = live.xpath("a/div[2]/p/@title")[0]
        people_number = live.xpath("a/div[1]/div/div[5]/div/div/span/span/text()")[0]
        user_name = live.xpath("a/div[3]/a/text()")[0]
        print("直播间名称 = %s \n用户名 = %s \n直播间人数 = %s \n直播间ID = %s \n" % (live_name, user_name, people_number, live_id))


def get_next_page(count: int, offset: int):
    params = {
        "aid": "6383",
        "live_id": "1",
        "device_platform": "web",
        "language": "zh-CN",
        "cookie_enabled": "true",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "108.0.0.0",
        "count": count,
        "offset": offset,
        "partition": "720",
        "partition_type": "1",
        "msToken": "",
        "X-Bogus": "",
        "_signature": "",
    }
    requests.get(NEXT_PAGE_URL, params=params)


def get_all_hot_lives():
    get_index_page_hot_lives()


if __name__ == '__main__':
    get_all_hot_lives()
