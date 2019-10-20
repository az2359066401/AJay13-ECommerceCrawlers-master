# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import csv
import os
import queue

import requests
from lxml import etree

from utils.utils import get_header
import  pymysql


from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import re
import random
import time

conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 30)


def get_detail_info(self,job_url):
    browser.get(job_url)
    htmlStr = browser.page_source
    detail_info = pq(htmlStr)
    divs = detail_info('.detail-content .job-sec')
    i = 0
    detail = ''
    gongsi = ''
    gongshang = ''
    for item in divs.items():
        if  i==0:
            # 职位信息
            detail = item('.job-sec').text().strip()
        if  i==1:
            # 公司介绍
            gongsi = item('.company-info').text().strip()
        if  i==3:
            #工商信息
            gongshang = item('.job-sec').text().strip()
            break
        i+=1
    self.detail = detail
    self.gongsi = gongsi
    self.gongshang = gongshang

class Boss(object):
    '''
    Boss直聘
    '''

    def __init__(self, keyword, city, path=os.getcwd()):
        self.keyword = keyword
        self.city = city
        self.path = path
        self.base_url = 'https://www.zhipin.com/'
        self.jobqueue = queue.Queue()
        self.csv_header = ['职位名称', '职位链接', '公司名称', '工作地点', '薪资', '工作经验', '学历要求', '所属领域', '公司状态',
                           '公司规模', '发布人', '职位信息', '公司介绍', '工商信息']
        self.downloadqueue = queue.Queue()

    def _get_city_code(self):
        url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
        req = requests.get(url=url, headers=get_header()).json()
        if req['message'] == 'Success':
            city_code_dict = req.get('zpData').get('cityList')
            for i in city_code_dict:
                for c in i['subLevelModelList']:
                    if c['name'] == self.city:
                        return str(c['code'])
            return '100010000'  # 全国




    def Spider(self):
        for page in range(1, 101):
            params = {
                'query': self.keyword,
                'page' : page
            }
            # req = requests.get(url=self.base_url + 'c' +self._get_city_code(), params=params, headers=get_header())
            # print(req.url)
            # html = etree.HTML(req.text)

            browser.get("https://www.zhipin.com/c101280600?query="+self.keyword+"&page=" + str(page))
            htmlStr = browser.page_source
            html = pq(htmlStr)
            divs = html('.job-primary')
            for item in divs.items():
                # 招聘职位
                title = item('.job-title').text()

                # 薪资
                salery = item('.red').text()

                awe = item('.info-primary p')
                awe = str(awe)
                result = re.match('^<p>(.*?)<em.*?e"/>(.*?)<em.*?e"/>(.*?)</p>', awe, re.S)
                if  result:
                    # 公司地址
                    area = result.group(1)

                    # 工作经验
                    exp = result.group(2)

                    # 学历
                    study = result.group(3)

                # 公司简称
                name = item('.company-text h3').text()

                pfn = item('.info-company .company-text p')
                pfn = str(pfn)
                result = re.match('^<p>(.*?)<em.*?e"/>(.*?)<em.*?e"/>(.*?)</p>', pfn, re.S)

                if  result:
                    # 行业
                    belong = result.group(1)

                    # 融资状况
                    status = result.group(2)

                    # 公司人数
                    size = result.group(3)

                # 联系人
                Hr = item('.info-publis h3').text()

                # 发布时间
                pub_time = item('.info-publis p').text()

                link = 'https://www.zhipin.com' + item('.info-primary a').attr('href')

                # 职位描述+任职资格
                get_detail_info(self,link)
                detail = self.detail
                gongsi = self.gongsi
                gongshang =self.gongshang

                # writer.writerow((title, company_short_Name, salary, addr, workEx, edu, detail, profess, finace,
                #                  num_person, contacts, pub_time, job_url))

                time.sleep(random.randrange(1, 4))

                data = {}
                data.update(职位名称=title, 公司名称=name, 职位链接=link, 工作地点=area, 薪资=salery, 工作经验=exp, 学历要求=study,
                            所属领域=belong, 公司状态=status, 公司规模=size, 发布人=Hr, 职位信息=detail, 公司介绍=gongsi,
                            工商信息=gongshang)
                self.downloadqueue.put(data)

                insert_sql = """
                insert into boss(title,name,link,area,salery,exp,study,belong,status,size,Hr,detail,gongsi,gongshang) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(insert_sql, (title,name,link,area,salery,exp,study,belong,status,size,Hr,detail,gongsi,gongshang))
                conn.commit()


    def run(self):
        data = []
        if os.path.exists(self.path):
            self.path = os.path.join(self.path, 'save-data')
            self.Spider()
            # while not self.downloadqueue.empty():
            #     data.append(self.downloadqueue.get())
            # with open(os.path.join(self.path, 'Boss直聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
            #           newline='', encoding='gb18030') as f:
            #     f_csv = csv.DictWriter(f, self.csv_header)
            #     f_csv.writeheader()
            #     f_csv.writerows(data)

if __name__ == '__main__':
    a = Boss(keyword='大数据', city='深圳').run()
