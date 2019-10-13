#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
import pymysql
# 定义请求url
url = "https://movie.douban.com/j/search_subjects"
# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8mb4", use_unicode=True)
cursor = conn.cursor()
response = requests.get("https://movie.douban.com/j/search_tags?type=movie&tag=%E6%9C%80%E6%96%B0&source=index")
tags=json.loads(response.text).get('tags')

# 循环构建请求参数并且发送请求
for tag in tags:
    for page_start in range(0, 100, 20):
        params = {
            "type": "movie",
            "tag": tag,
            "sort": "recommend",
            "page_limit": "20",
            "page_start": page_start
        }
        print(str(params))
        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )
        # 方式一:直接转换json方法
        # results = response.json()
        # 方式二: 手动转换
        # 获取字节串
        content = response.content
        # 转换成字符串
        string = content.decode('utf-8')
        # 把字符串转成python数据类型
        results = json.loads(string)
        # 解析结果
        for movie in results["subjects"]:
            print(tag,movie["title"], movie["rate"])
            insert_sql = """
            insert into douban_movie(tag,title,rate) values (%s,%s,%s)
            """
            cursor.execute(insert_sql, (tag,movie["title"], movie["rate"]))
            conn.commit()