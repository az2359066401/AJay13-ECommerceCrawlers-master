# -*- coding: utf-8 -*-
# author：zjp

"""
通过国家统计局官网获取中国2018年所有城市数据
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/
"""
import re
import requests
import time
import sys

fileSavePath = 'F://data/China_Province_2018.txt'  # 数据储存路径
fileSavePath2 = 'F://data/China_Province_2018_mistake.txt'  # 错误信息储存路径
results2 = []
results3 = []
results4 = []
results5 = []
Dates1 = []

n = 0
# 获取一级城市信息
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'
response = requests.get(url)
response.raise_for_status()  # 如果 HTTP 请求返回了不成功的状态码,Response.raise_for_status() 会抛出一个 HTTPError异常
response.encoding = response.apparent_encoding  # response.apparent_encoding从内容中分析出的响应内容编码方式
pattern = re.compile("<a href='(.*?)'>(.*?)<")
result1 = list(set(re.findall(pattern, response.text)))  # 从首层页面获取进入第二层页面的html
# print('result1')
# print(result1)

# 从一级城市获取二级城市信息
for cycle1 in range(len(result1)):
    try:
        url1 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{0}'.format(result1[cycle1][0])  # 一级城市url
        address1 = result1[cycle1][1]  # 一级城市
        # print('{0}  {1}'.format(address1, url1))
        response1 = requests.get(url1)
        response1.raise_for_status()
        response1.encoding = response1.apparent_encoding
        response1.close()
        pattern1 = re.compile("<a href='(.*?)'>(.*?)<")  # 正则表达式提取目标字段
        result2_1 = list(set(re.findall(pattern1, response1.text)))
        result2 = []
        for result in result2_1:  # 爬取的城市信息和城市代码混在一起，需要将代码清除
            if '0' not in result[1]:
                result2.append(result)
    # print('result2')
    # print(result2)
    except:
        print("Unexpected error:", sys.exc_info())
        with open(fileSavePath, 'a', encoding='utf-8')as f:
            f.write('{0}|一级错误|一级错误|一级错误|{1}\n'.format('xd', sys.exc_info()))
            f.close()
        time.sleep(10)
        continue
    # 从二级城市获取三级城市信息
    for cycle2 in range(len(result2)):
        try:
            address2 = result2[cycle2][1]  # 二级城市
            url2 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{0}'.format(result2[cycle2][0])  # 二级城市url
            # print(url2)
            response2 = requests.get(url2)
            response2.raise_for_status()
            response2.encoding = response2.apparent_encoding
            response2.close()
            pattern2 = re.compile("<a href='(.*?)'>(.*?)<")
            result3_1 = list(set(re.findall(pattern2, response2.text)))
            result3 = []
            for result in result3_1:
                if '0' not in result[1]:
                    result3.append(result)
        # print('result3')
        # print(result3)
        except:
            print("Unexpected error:", sys.exc_info())
            with open(fileSavePath, 'a', encoding='utf-8') as f:
                f.write('{0}|二级错误|二级错误|二级错误|{1}\n'.format(address1, sys.exc_info()))
                f.close()
            time.sleep(10)
            continue
        # 从三级城市获取四级城市信息
        for cycle3 in range(len(result3)):
            try:
                address3 = result3[cycle3][1]  # 三级城市
                url3 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/{0}/{1}' \
                    .format(result3[cycle3][0][3:5], result3[cycle3][0])  # 三级城市url
                response3 = requests.get(url3)
                response3.raise_for_status()
                response3.encoding = response3.apparent_encoding
                response3.close()
                pattern3 = re.compile("<a href='(.*?)'>(.*?)<")
                result4_1 = list(set(re.findall(pattern3, response3.text)))
                result4 = []
                for result in result4_1:
                    if '0' not in result[1]:
                        result4.append(result)
            # print('result4')
            # print(result4)
            except:
                print("Unexpected error:", sys.exc_info())
                with open(fileSavePath, 'a', encoding='utf-8')as f:
                    f.write('{0}|三级错误|三级错误|三级错误|{1}\n'.format(address2, sys.exc_info()))
                    f.close()
                time.sleep(10)
                continue
            # 从四级城市获取四五级城市信息
            for cycle4 in range(len(result4)):
                try:
                    address4 = result4[cycle4][1]  # 四级城市
                    url4 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/{0}/{1}/{2}' \
                        .format(result4[cycle4][0][3:5], result4[cycle4][0][5:7], result4[cycle4][0])  # 四级城市url
                    response4 = requests.get(url4)
                    response4.raise_for_status()
                    response4.encoding = response4.apparent_encoding
                    response4.close()
                    time.sleep(1)
                    pattern4_1 = re.compile("<a href='(.*?)'>(.*?)<")
                    # 可能已经到最后一层
                    pattern4 = re.compile("<tr class='villagetr'><td>.*?</td><td>.*?</td><td>(.*?)</td></tr>")
                    result5_1 = list(set(re.findall(pattern4, response4.text)))
                    result5 = []
                    for result in result5_1:
                        if '0' not in result[1]:
                            result5.append(result)
                    print('result5')
                    print(result5)
                    if result5:
                        for cycle5 in result5:
                            address = '{0}|{1}|{2}|{3}|{4}'.format(address1, address2, address3, address4, cycle5)
                            print(address)
                            with open(fileSavePath, 'a', encoding='utf-8')as f:
                                f.write(address)
                                f.write('\n')
                                f.close()
                    else:
                        print('此处第五层城市结果为空,网址为: {0}'.format(url4))
                        with open(fileSavePath2, 'a', encoding='utf-8')as f2:
                            f2.write('此处第五层城市结果为空,网址为: {0}'.format(url4))
                            f2.close()
                except:
                    print("Unexpected error:", sys.exc_info())
                    with open(fileSavePath, 'a', encoding='utf-8')as f:
                        f.write('{0}|四级错误|四级错误|四级错误|{1}\n'.format(address3, sys.exc_info()))
                        f.close()
                    time.sleep(10)
                    continue
print('well_done')

