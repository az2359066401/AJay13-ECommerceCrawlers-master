# -*- coding: utf-8 -*-
import requests
import sys
import re
from bs4 import BeautifulSoup
import pymysql
conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()


headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Cookie": "AD_RS_COOKIE=20081945; _trs_uv=jrhivtz7_6_jyyw",
"Host": "www.stats.gov.cn",
"If-Modified-Since": "Thu, 05 Jul 2018 00:43:11 GMT",
"If-None-Match": "17b5-57035d4e665c0-gzip",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
fileSavePath = 'F://data/China_City_2018.txt'  # 数据储存路径


def getItem(itemData, dataArray, parentRequestUrl, table, type):
    item = {}
    # 名称
    if(type == 5):
        item['name'] = str(dataArray[2].get_text())
    else:
        item['name'] = str(dataArray[1].get_text())
    # 下一级请求url
    href = re.findall('(.*)/', parentRequestUrl)
    if type != 5:
        item['url'] = href[0] + "/" + dataArray[0].get('href')
    # 父级code
    item['parentCode'] = itemData.get('code')
    # 类型
    item['type'] = type
    # code码
    item['code'] = str(dataArray[0].get_text())[0:12]
    # if type == 4:
    #     print(item.get('url'))
    # 打印出sql语句
    print('insert into %s(name,code,type,parent_code) values (%s,%s,%s,%s)' % (
        table, "'"+item['name'] +"'", "'"+item['code']+"'", item['type'], "'"+item['parentCode']+"'") + ";")
    insert_sql = 'insert into %s(name,code,type,parent_code) values (%s,%s,%s,%s)' % (
        table, "'"+item['name'] +"'", "'"+item['code']+"'", item['type'], "'"+item['parentCode']+"'") + ";"
    cursor.execute(insert_sql)
    conn.commit()
    return item

# 获取BeautifulSoup
def getSoup(requestUrl):
    htmls = requests.get(requestUrl, headers=headers)
    htmls.encoding = 'GBK'
    soup = BeautifulSoup(htmls.text, 'html.parser', from_encoding='UTF-8')
    return soup

# 循环处理
def loopItem(label, labelClass, labelChild, item, requestUrl, type, tableName, lists):
    for link in soup.find_all(label, labelClass):
        array = link.find_all(labelChild, class_='')
        if not len(array):
            continue
        itemData = getItem(item, array, requestUrl, tableName, type)
        lists.append(itemData)

requestProviceUrl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'
soup = getSoup(requestProviceUrl)
# 省列表
provinceList = []
for link in soup.find_all('a', class_=''):
    requestCityUrl = re.findall('(.*)/', requestProviceUrl)
    item = {}
    # 名称
    item['name'] = str(link.get_text())
    # 下一级请求url
    href = str(link.get('href'))
    item['url'] = requestCityUrl[0] + "/" + href
    # 父级code
    item['parentCode'] = '000000000000'
    # 类型
    item['type'] = 1
    # code码
    item['code'] = (href.split('.'))[0] + '0000000000'
    provinceList.append(item)
    # 打印出sql语句
    # print('====>',types)
    print('insert into province(name,code,type,parent_code) values (%s,%s,%s,%s)' % (
        ("'"+item['name'] +"'"+ ''), "'"+item['code']+"'", item['type'], "'"+item['parentCode']+"'") + ";")
    insert_sql = 'insert into province(name,code,type,parent_code) values (%s,%s,%s,%s)' % (
        ("'"+item['name'] +"'"+ ''), "'"+item['code']+"'", item['type'], "'"+item['parentCode']+"'") + ";"
    cursor.execute(insert_sql)
    conn.commit()
# 市列表
cityList = []
for item in provinceList:
    # 测试正常退出
    cityRequestUrl = str(item.get('url'))
    soup = getSoup(item.get('url'))
    loopItem('tr', 'citytr', 'a', item, cityRequestUrl, 2, 'city', cityList)

# 县列表
countyList = []
for item in cityList:
    # 测试正常退出
    countyRequestUrl = str(item.get('url'))
    soup = getSoup(item.get('url'))
    loopItem('tr', 'countytr', 'a', item,
     countyRequestUrl, 3, 'county', countyList)

# 城镇列表
townList = []
for item in countyList:
    # 测试正常退出
    townRequestUrl = str(item.get('url'))
    soup = getSoup(item.get('url'))
    loopItem('tr', 'towntr', 'a', item, townRequestUrl, 4, 'town', townList)

# 村庄列表
villageList = []
for item in townList:
    # 测试正常退出
    villageRequestUrl = str(item.get('url'))
    soup = getSoup(item.get('url'))
    loopItem('tr', 'villagetr', 'td', item,
     villageRequestUrl, 5, 'village', villageList)
