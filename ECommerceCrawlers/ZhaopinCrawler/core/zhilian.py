# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

import requests
from utils.utils import get_header
import csv
import os
from lxml.html import etree
import config

import pymysql

conn = pymysql.connect('localhost', 'root', '123456', 'article_spider', charset="utf8", use_unicode=True)
cursor = conn.cursor()


class ZhiLian(object):
    '''
    智联招聘
    :param
    构造函数:
    传入：搜索职业关键字、招聘地点
    调用run方法：返回csv文件
    '''
    def __init__(self, keyword, page=100, city='全国', path=os.getcwd()):
        self.keyword = keyword
        self.page = page
        self.base_url = 'https://fe-api.zhaopin.com/c/i/sou'
        self.city = city
        self.csv_header = ['ID', '工作名称', '招聘详细链接', '公司名称', '公司ID', '公司性质', '公司规模', '公司招聘主页',
                           '公司地点', '薪资', '学历要求', '工作经历', '职位类型', '公司福利', '工作发布标签', '更新时间', '职位描述']
        self.path = path


    def Spider(self):
        jobl = []
        for page in range(self.page):
            params = {
                "start": 90 * page,
                "pageSize": 90,
                "workExperience": -1,
                "education": -1,
                "companyType": -1,
                "employmentType": -1,
                "jobWelfareTag": -1,
                "kw": self.keyword,
                "kt": 3,
                "cityId": self.city,
                "salary": '0, 0'
            }
            req = requests.get(url=self.base_url, params=params, headers=get_header())
            cookie = req.cookies
            print(cookie)
            data = req.json()['data']['results']
            if len(data) != 0:
                for job in data:
                    # print(job)
                    jobd = {}
                    jobd['ID'] = job.get('number')
                    jobd['工作名称'] = job.get('jobName')
                    jobd['招聘详细链接'] = job.get('positionURL')
                    company = job.get('company')
                    jobd['公司名称'] = company.get('name')
                    jobd['公司ID'] = company.get('number')
                    jobd['公司性质'] = company.get('type').get('name')
                    jobd['公司规模'] = company.get('size').get('name')
                    jobd['公司招聘主页'] = company.get('url')
                    jobd['公司地点'] = job.get('city').get('display')
                    jobd['薪资'] = job.get('salary')
                    jobd['学历要求'] = job.get('eduLevel').get('name')
                    try:
                        jobd['工作经历'] = job.get('workingExp').get('name')
                    except:
                        jobd['工作经历'] = '经验不限'
                    jobd['职位类型'] = job.get('emplType')
                    jobd['公司福利'] = '、'.join(job.get('welfare')) or '无'
                    jobd['工作发布标签'] = job.get('timeState')
                    jobd['更新时间'] = job.get('updateDate')
                    header = get_header()
                    header['referer'] = job.get('positionURL')
                    header['upgrade-insecure-requests'] = '1'
                    ZHILIAN_COOKIE = 'adfbid2=0; x-zp-client-id=912a3ef6-bb0d-46c9-a396-ea9566250f8a; sts_deviceid=16bd0b9394299-0b310c2e8d3a19-e343166-2073600-16bd0b93943668; acw_tc=2760824a15648151356115930e8773f8ab7c33fc21043ce1c44b11cd7f5da1; _uab_collina=156481966519005574477937; urlfrom2=121114583; adfcid2=www.baidu.com; sou_experiment=capi; ZP_OLD_FLAG=false; CANCELALL=1; LastCity=%E5%8C%97%E4%BA%AC; LastCity%5Fid=530; dywea=95841923.417992036732763400.1562574932.1564819776.1564824996.3; dywez=95841923.1564824996.3.3.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1562574933,1564819776,1564824996; __utma=269921210.1630440294.1562574933.1564819776.1564824996.3; __utmz=269921210.1564824996.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216bd0b9395e473-06c4ddd9790ee2-e343166-2073600-16bd0b9395f866%22%2C%22%24device_id%22%3A%2216bd0b9395e473-06c4ddd9790ee2-e343166-2073600-16bd0b9395f866%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baiduPC%22%2C%22%24latest_utm_medium%22%3A%22CPC%22%2C%22%24latest_utm_campaign%22%3A%22pp%22%2C%22%24latest_utm_content%22%3A%22pp%22%2C%22%24latest_utm_term%22%3A%228804373%22%7D%7D; sts_sg=1; sts_chnlsid=Unknown; jobRiskWarning=true; sts_sid=16c5fc1dd9645-03591d4b89f0ab-e343166-2073600-16c5fc1dd97a91; acw_sc__=5d479f892414863f1ea95e2ce7352ba574fd9d2f; zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC120116927J00122526309.htm; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22de9c9056-061b-4d15-9b59-d930c831f19e-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}%2C%22company%22:{%22actionid%22:%22fe6b5ca0-7e6b-4587-874f-4f39773534a2-company%22%2C%22funczone%22:%22hiring_jd%22}}; sts_evtseq=14'
                    # header['cookie'] = config.ZHILIAN_COOKIE
                    header['cookie'] = ZHILIAN_COOKIE
                    req1 = requests.get(job.get('positionURL'), headers=header, )
                    req1.encoding = 'utf-8'
                    html = etree.HTML(req1.text)
                    detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]//*/text()'))
                    if not detail:
                        detail = ''.join(html.xpath('//*[@class="describtion__detail-content"]/text()'))
                    print(detail)
                    jobd['职位描述'] = detail.strip()

                    insert_sql = """
                    insert into zhilian(number ,jobName ,positionURL ,comName ,comNumber ,comType ,comSize ,comUrl ,comCity ,salary ,eduLevel ,workingExp ,emplType ,walfare ,timeState ,updateDate ,detail) 
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                    cursor.execute(insert_sql, (
                        job.get('number'),
                        job.get('jobName'),
                        job.get('positionURL'),
                        company.get('name'),
                        company.get('number'),
                        company.get('type').get('name'),
                        company.get('size').get('name'),
                        company.get('url'),
                        job.get('city').get('display'),
                        job.get('salary'),
                        job.get('eduLevel').get('name'),
                        job.get('workingExp').get('name') if job.get('workingExp') and job.get('workingExp').get('name') else '经验不限',
                        job.get('emplType'),
                        '、'.join(job.get('welfare')) or '无',
                        job.get('timeState'),
                        job.get('updateDate'),
                        detail.strip()
                        ))
                    conn.commit()
                    jobl.append(jobd)
            else:
                break
        return jobl

    def run(self):

        if os.path.exists(self.path):
            data = self.Spider()
            self.path = os.path.join(self.path, 'save-data')
            # with open(os.path.join(self.path, '智联招聘_关键词_{}_城市_{}.csv'.format(self.keyword, self.city)), 'w',
            #           newline='', encoding='utf-8-sig') as f:
            #     f_csv = csv.DictWriter(f, self.csv_header)
            #     f_csv.writeheader()
            #     f_csv.writerows(data)


if __name__ == '__main__':

    a = ZhiLian(keyword='python', city='厦门').run()
