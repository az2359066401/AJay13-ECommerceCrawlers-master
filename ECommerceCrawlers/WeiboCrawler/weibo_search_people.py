#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/3/26 0026'

"""

import re
import time
import pymysql

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 30)


def index_page(page, custom):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页，省份', custom)
    try:
        sec = 1
        while True:

            url = 'https://s.weibo.com/user?q={KEYWORD}&Refer=weibo_user&page={page}&region=custom:{custom}:{sec}'.format(
                KEYWORD=KEYWORD, page=page, custom=custom, sec=sec)

            browser.get(url)
            time.sleep(1)
            domain = get_products()
            sec += 1
            if not domain:
                break
    except TimeoutException:
        pass


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#pl_user_feedList .info').items()
    for item in items:
        text = item.text().replace('\n', '')
        pattern = '关注(\d*) 粉丝(.*?) 微博(\d*)'
        result = re.findall(pattern=pattern, string=text)
        follow = '0'
        fans = '0'
        weibo = '0'
        if result:
            follow = result[0][0]
            fans = result[0][1]
            weibo = result[0][2]
        s_nobr = item.find('.s-nobr')
        pattern = '>微博<a href="//weibo.com/(\d*)/profile'

        wid = re.findall(pattern=pattern, string=str(s_nobr))
        if wid:
            id = wid[0]
        else:
            id = (item.find('.name').attr('href')).replace('//weibo.com/u/', '')

        products = {
            'name': item.find('.name').text().replace('\n', ''),
            'domain': item.find('.name').attr('href'),
            'id': id,
            'follow': follow,
            'fans': fans,
            'weibo': weibo,
            'keyword': KEYWORD,

        }
        print(products)
        # save(str(products))
        select_sql = """
        select id from  weibo_search_people where id = {}
        """
        res = cursor.execute(select_sql.format(str("\"" + products['id'] + "\"")))
        conn.commit()
        print(res)
        if res == 0:
            insert_sql = """
            insert into weibo_search_people(id,keyword,name,domain,follow,fans,weibo) values (%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(insert_sql, (products['id'],products['keyword'],products['name'],products['domain'],products['follow'],products['fans'],products['weibo']))
            conn.commit()
    if len(doc('#pl_user_feedList .info')) > 0:
        return True
    else:
        return False


def save(products):
    with open('products.txt', 'a+', encoding='GBK')as f:
        f.write(products + '\n')


def main():
    for page in range(1, 51):
        for custom in [11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 37, 41, 43, 44, 45, 46, 50, 51, 52, 53, 54,
                       61, 62, 63, 64, 65, 71, 81, 82, 400]:
            index_page(page, custom)
    browser.close()


if __name__ == '__main__':
    KEYWORD = '房'
    # KEYWORD = '美妆'
    main()
