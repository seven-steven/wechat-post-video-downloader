#!/usr/bin env python3

import json
import sys
import threading

import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.15um.com",
    "Origin": "http://www.15um.com",
    "Referer": "http://www.15um.com/tools/weixin_v.php",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
api = 'http://www.15um.com/tools/weixin_v.php'
cookies = None


def get_cookie():
    """
    获取 cookies
    :return:
    """
    header = requests.get(api)
    return header.cookies


def get_video_list(wechat_url):
    """
    获取视频列表
    :param wechat_url:
    :return:
    """
    data = {'url': wechat_url}
    html = requests.post(api, data=data, headers=headers, cookies=cookies)
    videos = json.loads(html.text)

    return videos['data']


def download(video):
    """
    下载单个视频
    :param video: 视频地址
    """
    filename = video['title'] + ".mp4"
    with open(filename, 'wb') as f:
        video = requests.get(video['url'], stream=True)
        print("\t开始下载:\t" + filename)
        for chunk in video.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        print("\t视频:\t" + filename + "\t 下载完成!")


def line(wechat_url_list):
    """
    控制器, 根据给出的 url 列表下载视频
    :param wechat_url_list:
    :return:
    """
    thread_list = list()
    for url in wechat_url_list:
        print("开始下载: " + url)
        video_list = get_video_list(url)
        for video in video_list:
            print("\t发现视频:" + video.get('title'))
            thread_list.append(threading.Thread(target=download, args=(video,)))

    # 启动下载线程
    for thread in thread_list:
        thread.start()
    # 将下载线程加入主线程
    for thread in thread_list:
        thread.join()


if __name__ == "__main__":
    cookies = get_cookie()
    line(sys.argv[1:])
    print("========= 下载完毕! =========")
