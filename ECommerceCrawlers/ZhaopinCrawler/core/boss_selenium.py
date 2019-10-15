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



conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 30)

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
        for page in range(1, 11):
            params = {
                'query': self.keyword,
                'page' : page
            }
            # req = requests.get(url=self.base_url + 'c' +self._get_city_code(), params=params, headers=get_header())
            # print(req.url)
            # html = etree.HTML(req.text)

            browser.get("https://www.zhipin.com/c101280600?query=java&page=" + str(page))
            htmlStr = browser.page_source
            html = pq(htmlStr)

            if page == 1:
                for i in range(1, 30):
                    title = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/h3/a/div[1]'.format(i)).text
                    link = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/h3/a'.format(i)).get_attribute('href')
                    name = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div/h3/a'.format(i)).text
                    data1 = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/p'.format(i)).text.split(' ')
                    area = data1[0]
                    salery = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[1]/h3/a/span'.format(i)).text
                    exp = data1[1]
                    study = data1[2]
                    belong = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div/p'.format(i)).text
                    status = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div/p'.format(i)).text
                    try: size = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[2]/div/p'.format(i)).text
                    except: size = '无'
                    Hr = browser.find_element_by_xpath('//*[@id="main"]/div/div[3]/ul/li[{}]/div/div[3]/h3'.format(i)).text
                    req1 = requests.get(url=link, headers=get_header())
                    req1.encoding = 'utf-8'
                    html1 = etree.HTML(req1.text)
                    detail = ''.join(html1.xpath('//*[@class="job-sec"][1]//*/text()')).strip()
                    if detail.isspace():
                        detail = ''.join(html1.xpath('//*[@class="job-sec"][1]/text()')).strip()
                    print(detail)
                    gongsi = ''.join(html1.xpath('//*[@class="job-sec company-info"]//*/text()')).strip()
                    gongshang = ''.join(html1.xpath('//*[@class="job-sec"][3]//*/text()')).strip()
                    if '点击查看地图' in gongshang:
                        gongshang = ''.join(html1.xpath('//*[@class="job-sec"][2]//*/text()')).strip()
                    data = {}
                    data.update(职位名称=title, 公司名称=name, 职位链接=link, 工作地点=area, 薪资=salery, 工作经验=exp, 学历要求=study,
                                所属领域=belong, 公司状态=status, 公司规模=size, 发布人=Hr, 职位信息=detail, 公司介绍=gongsi, 工商信息=gongshang)
                    self.downloadqueue.put(data)
            else:
                try:
                    for i in range(1,31):
                        title = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/h3/a/div[1]/text()'.format(i))[0]
                        name = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/h3/a/text()'.format(i))[0]
                        link = self.base_url.rstrip('/') + html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/h3/a/@href'.format(i))[0]
                        data1 = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/p/text()'.format(i))
                        area = data1[0]
                        salery = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[1]/h3/a/span/text()'.format(i))[0]
                        exp = data1[1]
                        study = data1[2]
                        belong = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/p/text()[1]'.format(i))[0]
                        status = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/p/text()[2]'.format(i))[0]
                        try:
                            size = \
                            html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/p/text()[3]'.format(i))[0]
                        except: size = '无'
                        who = html.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[3]/h3/text()[1]'.format(i))[0]
                        try:
                            job = html.xpath('//*[@id="main"]/div/div[2]/ul/li[1]/div/div[3]/h3/text()[2]'.format(i))[0]
                        except:
                            job = '无'
                        Hr = '{}/{}'.format(who, job)
                        req1 = requests.get(url=link, headers=get_header())
                        req1.encoding = 'utf-8'
                        html1 = etree.HTML(req1.text)
                        detail = ''.join(html1.xpath('//*[@class="job-sec"][1]//*/text()')).strip()
                        gongsi = ''.join(html1.xpath('//*[@class="job-sec company-info"]//*/text()')).strip()
                        gongshang = ''.join(html1.xpath('//*[@class="job-sec"][3]//*/text()')).strip()
                        if '点击查看地图' in gongshang:
                            gongshang = ''.join(html1.xpath('//*[@class="job-sec"][2]//*/text()')).strip()
                        print(detail)
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
                except Exception as e:
                    continue
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
    a = Boss(keyword='java', city='深圳').run()
