import urllib
import requests
import sys
import re
from bs4 import BeautifulSoup
import pymysql
from lxml import etree
i=0
for n in range(10):
     url = r'http://sousuo.gov.cn/s.htm?t=govall&advance=false&n=10&p='+str(n)+'&timetype=&mintime=&maxtime=&sort=&q=%E8%80%81%E9%BE%84%E5%8C%96'
     #url = r'http://sousuo.gov.cn/s.htm?q=&n=10&p='+str(n)+'&t=paper&advance=true&title=%E5%85%BB%E8%80%81&content=&puborg=&pcodeJiguan=&pcodeYear=&pcodeNum=&childtype=&subchildtype=&filetype=&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&nocorrect='         #指定要抓取的网页url，必须以http开头
     res = urllib.request.urlopen(url)  #调用urlopen()从服务器获取网页响应(respone)，其返回的响应是一个实例
     html = res.read().decode('utf-8')  #调用返回响应示例中的read()，可以读取html
     soup = BeautifulSoup(html, 'lxml')
     result = soup.find_all('div',class_ = 'result')#result = soup.find_all('div',class_ = 'result')
     #print(result)
     #使用查询结果再创建一个BeautifulSoup对象,对其继续进行解析
     download_soup = BeautifulSoup(str(result), 'lxml')
     urls=[]
     url_all = download_soup.find_all('a')
     for a_url in url_all:
            a_url = a_url.get('href')
            urls.append(a_url)
            print(a_url)
            if a_url and a_url.startswith('http'):
                req = requests.get(url=a_url)
                print(req.url)

                htmlz = etree.HTML(req.content.decode('utf-8'))
                text = htmlz.xpath('//*[@id="UCAP-CONTENT"]/p/text()')
                textstr = ''.join(text).strip()
                w=open(str(i) + '.txt','w',encoding='utf-8')
                i=i+1
                w.write(textstr)
                w.close()
print('finish')
