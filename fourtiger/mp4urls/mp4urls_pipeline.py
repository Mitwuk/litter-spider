# -*-coding:utf-8-*-
# @time: 2020/5/10 12:16
# @author: Mitwuk
# @description: 持久层

from commons.mysql_helper import MysqlHelper


class Mp4urlsPipeline(object):
    def __init__(self):
        self.mysql = MysqlHelper()

    def query_tiger_url(self):
        """
        url作为唯一标识
        :return:
        """
        sql = "select id, url, http_url from tiger where http_url is null and id > 20205"
        return self.mysql.query(sql)

    def update_http_url(self, t_id, http_url):
        sql = "update tiger set http_url = '%s' where id = %s" % (http_url, t_id)
        self.mysql.execute(sql)
