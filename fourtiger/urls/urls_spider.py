# -*-coding:utf-8-*-
# @time: 2020/5/10 12:06
# @author: Mitwuk
# @description: 获取fourtiger的url列表

from time import sleep

import requests
from bs4 import BeautifulSoup

from commons.log_helper import LogHelper
from fourtiger.settings import *
from urls.urls_pipeline import UrlsPipeline


def get_nums():
    """
    页码导向
    国产区：2-8
    亚洲五码：10-15,9/html22,34
    中文有嘛：16
    名优：18-25,35-42
    动画：26
    欧美：27
    :return:
    """
    gc_num = [n for n in range(2, 9)]
    wm_num = [n for n in range(12, 16)]
    wm_num.append('9/html22')
    wm_num.append(34)
    ym_num = [16]
    my_num = []
    my_num.extend([n for n in range(18, 22)])
    my_num.extend([n for n in range(23, 26)])
    my_num.extend([n for n in range(35, 42)])
    dh_page = [26]
    om_num = [27]
    nums = []
    nums.extend(my_num)
    nums.extend(ym_num)
    nums.extend(wm_num)
    nums.extend(dh_page)
    nums.extend(gc_num)
    nums.extend(om_num)
    return nums


class UrlsSpider(object):
    def __init__(self):
        self.log = LogHelper(log_file='log/tiger.log', log_name='tiger').get_logger()
        self.pipeline = UrlsPipeline()
        self.page = 10
        self.url_set = self.url_queue()

    def spider(self):
        nums = get_nums()
        for n in nums:
            list_url = '%s/vod/html%s' % (INIT_URL, n)
            while True:
                try:
                    response = requests.get(list_url).content.decode('utf8')
                    soup = BeautifulSoup(response, 'lxml')
                    a_list = soup.select('#dtextlink a')
                    mark1 = a_list[1].get_text()
                    mark2 = ""
                    items = soup.select('.col-md-2.col-sm-3.col-xs-4')
                    for item in items:
                        item_a = item.select_one("a")
                        photo_url = item_a.get("data-original")
                        url = item_a.get("href")
                        if url in self.url_set:
                            continue
                        overflow = item.select_one('.text-overflow')
                        title = overflow.get_text()
                        item_time = item.select_one('.note.text-bg-r')
                        update_time = item_time.get_text()
                        self.url_set.add(url)
                        self.pipeline.insert_tiger(mark1, mark2, title, url, photo_url, update_time)
                    lis = soup.select('.box-page.clearfix ul li')
                    if len(lis) < 2:
                        break
                    style = lis[-2].select_one('a').get('style')
                    if style:
                        break
                    list_url = '%s%s' % (INIT_URL, lis[-2].find("a").get('href'))
                    sleep(1)
                except Exception as err:
                    self.log.error(err.args)
                    self.log.error(list_url)

    def url_queue(self):
        """
        获取已抓取的URL作为去重队列
        :return:
        """
        url_set = set()
        query = self.pipeline.query_tiger_url()
        for item in query:
            url_set.add(item['url'])
        return url_set


if __name__ == "__main__":
    UrlsSpider().spider()
