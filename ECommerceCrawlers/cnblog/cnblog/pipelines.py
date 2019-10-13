# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  pymysql
import json
import time

class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        titles = item['title']
        links = item['link']
        for i, j in zip(titles, links):
            insert_sql = """
            insert into cnblog(title,link) values (%s,%s)
            """
            self.cursor.execute(insert_sql,(i,j))
            self.conn.commit()
        return item

