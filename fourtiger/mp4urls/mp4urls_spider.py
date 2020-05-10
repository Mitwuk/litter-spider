# -*-coding:utf-8-*-
# @time: 2020/5/10 12:06
# @author: Mitwuk
# @description: 获取fourtiger的mp4下载链接

import requests
from bs4 import BeautifulSoup

from commons.log_helper import LogHelper
from fourtiger.settings import *
from mp4urls.mp4urls_pipeline import Mp4urlsPipeline


def split_time(url):
    items = url.split('/')
    items.pop(3)
    url_new = ''
    for item in items:
        if item:
            url_new += '/' + item
    return url_new


class Mp4urlsSpider(object):
    def __init__(self):
        self.log = LogHelper(log_file='log/mp4urls.log', log_name='mp4urls').get_logger()
        self.pipeline = Mp4urlsPipeline()

    def spider(self):
        query = self.pipeline.query_tiger_url()
        for q in query:
            try:
                tiger_id = q.get("id")
                t_url = q.get("url").replace(".html", "_down_1.html")
                # t_url = split_time(t_url)
                url = INIT_URL + t_url
                response = requests.get(url).content.decode("utf8")
                soup = BeautifulSoup(response, "lxml")
                download_soup = soup.select_one('.download a')
                http_url = download_soup.get("href")
                print(http_url)
                self.pipeline.update_http_url(tiger_id, http_url)
            except Exception as err:
                self.log.error(err.args)


if __name__ == "__main__":
    Mp4urlsSpider().spider()
