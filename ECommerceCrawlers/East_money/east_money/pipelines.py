# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import pymysql

class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item['title']
        href = item['href']
        summary = item['summary']
        content = item['content']
        insert_sql = """
        insert into eastmoney(title,href,summary,content) values (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(title,href,summary,content))
        self.conn.commit()
        return item
