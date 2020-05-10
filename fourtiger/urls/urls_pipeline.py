# -*-coding:utf-8-*-
# @time: 2020/5/10 12:16
# @author: Mitwuk
# @description: 持久层

from commons.mysql_helper import MysqlHelper


class UrlsPipeline(object):
    def __init__(self):
        self.mysql = MysqlHelper()

    def insert_tiger(self, mark1, mark2, title, url, photo_url, update_time):
        sql = """
            insert into tiger (mark1, mark2, title, url, photo_url, update_time)
            VALUES ('{0}','{1}','{2}','{3}','{4}', '{5}')
        """.format(mark1, mark2, title, url, photo_url, update_time)
        self.mysql.execute(sql)

    def query_tiger_url(self):
        """
        url作为唯一标识
        :return:
        """
        sql = "select id, url, http_url from tiger"
        return self.mysql.query(sql)
