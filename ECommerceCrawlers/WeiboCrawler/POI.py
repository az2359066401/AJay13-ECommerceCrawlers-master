# -*- coding: utf-8 -*-
#-----------------采集全重庆范围内的POI兴趣点-------------------
import requests
import json
import xlrd
import pandas as pd
import pymysql
import time

def sleeptime(day=1): # 默认参数智能放最后
    return day * 24 * 3600

def get_Region():
    #'重庆市渝中区',
    region = ['重庆市渝中区','重庆市江北区','重庆市渝北区','重庆市沙坪坝区','重庆市九龙坡区',
              '重庆市南岸区','重庆市巴南区','重庆市北碚区','重庆市大渡口区']

    lng_lat = {'重庆市渝中区':'29.525375,106.494032,29.582745,106.602727',  #重庆市渝中区的矩形区域左下角和右上角的经纬度（可参看百度文档对矩形区域的解释）
               '重庆市江北区':'29.571878,106.440282,29.689841,106.896587',  #左下：106.440282,29.571878
               '重庆市渝北区':'29.575192,106.434211,30.051651,106.993128',  #右上106.993128,30.051651
               '重庆市沙坪坝区':'29.497572,106.261671,29.755899,106.51607',  #106.275683,29.497572
               '重庆市九龙坡区': '29.248442,106.275683,29.574961,106.553261',
               '重庆市南岸区':'29.476615,106.542511,29.614757,106.803882',
               '重庆市巴南区':'29.118686,106.520931,29.735054,107.062741',
               '重庆市北碚区':'29.66131,106.29192,30.109513,106.720972',
               '重庆市大渡口区':'29.344094,106.403174,29.509104,106.532859'}

               #'重庆市渝中区':'29.525375,106.494032,29.582745,106.602727',  #右上 106.597337,29.578724
               # '重庆市江北区':'29.571878,106.440282,29.689841,106.896587',  #左下：106.440282,29.571878
               # '重庆市渝北区':'29.575192,106.434211,30.051651,106.993128',  #右上106.993128,30.051651
               # '重庆市沙坪坝区':'29.497572,106.261671,29.755899,106.51607', #106.275683,29.497572
               #'重庆市九龙坡区':'29.248442,106.275683,29.574961,106.553261'#, #106.275683,29.248442,106.553261,29.574961
               # '重庆市南岸区':'29.476615,106.542511,29.614757,106.803882',
               # '重庆市巴南区':'29.118686,106.520931,29.735054,107.062741',
               # '重庆市北碚区':'29.66131,106.29192,30.109513,106.720972',
               # '重庆市大渡口区':'29.344094,106.403174,29.509104,106.532859'}#各行政区左下右上经纬度
    return region,lng_lat

#
# 左下角： [29.547183, 106.545379]
# 右上角:  [29.5560735, 106.559716]

def get_Keyword():
    #path =r'E:\Project\电子围栏\Data\兴趣点.xlsx'
    #data = pd.read_excel(path,sheet_name='keyword2')
    data = ['酒店','公司']
    data = {"keyword":'酒店'}
    return data

def get_ak():#改成你自己的ak
    ak = ['xYhFWBgDCF12nPU5v2pMue5uN14d****',
          'nryXXcwxdwGws64qmB9jFE29yY6P****',
          'tP4RTTuWu0Rds81Hvm0Mn9QXajBs****',
          'GP12Wh7S1pM1oa4oNyib7xByol5X****']
    return ak

def get_Url(data,region,lng_lat,aks,connect):

    url_POI = 'http://api.map.baidu.com/place/v2/search?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ak_num = 0
    ak = aks[ak_num]
    payload = {'output': 'json'}
    payload['ak'] = ak
    payload['city_limit'] = 'true' #区域数据限制（只返回指定区域的信息）
    payload['scope'] = '2' # 返回详细信息，1或空为基本信息
    payload['page_size'] = '20' #每一页最多返回20个兴趣点
    for i in range(len(region)):
        payload['region'] = region[i] #指定行政区域名称
        trapeze = lng_lat[region[i]].split(',') #指定行政区的左下右上经纬度 trapeze 经纬度格

        #以下是将一个行政区（大矩形）划分为多个矩形网格，获取大于400个兴趣点的返回值
        left_bottom = [trapeze[0],trapeze[1]] #左下角坐标
        right_top = [trapeze[2],trapeze[3]]   #右上角坐标
        part_n = 20; #网格切割数量，20*20=400   可根据行政区域的大小调整网格数量

        x_item = (float(right_top[0]) - float(left_bottom[0])) / part_n; #纬度平均分割大小
        print(x_item)
        y_item = (float(right_top[1]) - float(left_bottom[1])) / part_n; #经度平均分割大小
        print(y_item)
        for key in range(len(data['keyword'])):
            payload['query'] = data['keyword'][key] #指定查询关键字
            #print(data['keyword'][key])
            for ii in range(part_n):  # 遍历横向网格
                for jj in range(part_n):  # 遍历纵向网格
                    #以下left_bottom_part、right_top_part认真理解
                    left_bottom_part = [float(left_bottom[0]) + ii * x_item, float(left_bottom[1]) + jj * y_item];  #切片的左下角坐标
                    right_top_part = [float(right_top[0]) - (part_n-1-ii) * x_item, float(right_top[1]) - (part_n-1-jj) * y_item];  # 切片的右上角坐标
                    for page_num in range(20): #接口最多返回20页
                        payload['page_num'] = page_num
                        payload['bounds']=str(left_bottom_part[0]) + ',' + str(left_bottom_part[1]) + ',' + \
                                          str(right_top_part[0])+','+str(right_top_part[1])
                        #print(payload)
                        try:
                            content = requests.get(url_POI,params=payload,headers=headers).json()
                            #print(content)
                            if content['status'] == 0: #能够正常返回值
                                if content['results']:
                                    storeTomysql(content, data['keyword'][key], connect,region[i])#存放数据库
                                else:
                                    break
                            else:
                                if content['status'] == 302:  # 如果ak配额用完
                                    print('第' + str(ak_num) + '个ak配额用完，自动调用下一个····')
                                    ak_num = ak_num+1
                                    if ak_num>(len(aks)-1):
                                        print('今天ak已用完，明天再继续吧。。。')
                                        time.sleep(sleeptime()) #程序休眠24小时
                                        ak_num = 0
                                        ak = aks[ak_num]
                                        payload['ak']=ak
                                        content = requests.get(url_POI, params=payload, headers=headers).json()
                                        if content['status']==0:
                                            if content['results']:
                                                storeTomysql(content,data['keyword'][key],connect,region[i])
                                            else:
                                                break #为空则跳出本层循环
                                        else:pass
                                    else:
                                        ak = aks[ak_num]
                                        payload['ak'] = ak
                                        content = requests.get(url_POI, params=payload, headers=headers).json()
                                        if content['status']==0:
                                            if content['results']:
                                                storeTomysql(content,data['keyword'][key],connect,region[i])
                                            else:
                                                break
                                        else:pass
                                else:
                                    pass #其他错误
                               # print(content)

                        except Exception as e:
                            print(e)



def mysql_Detail():
    # 使用的mysql数据库
    connect = pymysql.Connect(host='localhost', port=3306, user='root', passwd='123456',
                              db='article_spider', charset='utf8')
    return connect

def storeTomysql(content,Key_word,connect,region):
    #在 content 中提取详细信息
    # print('test01')
    cursor = connect.cursor()
    # if content['results']:
    for h in range(len(content['results'])):  # 遍历返回地点
        name = content['results'][h]['name']
        lng = content['results'][h]['location']['lng']
        lat = content['results'][h]['location']['lat']

        if 'area' in content['results'][h].keys():
            area = content['results'][h]['area']
        else:
            area = None
        if 'address' in content['results'][h].keys():
            address = content['results'][h]['address']
        else:
            address = None
        if 'province' in content['results'][h].keys():
            province = content['results'][h]['province']
        else:
            province = None
        if 'city' in content['results'][h].keys():
            city = content['results'][h]['city']
        else:
            city = None
        if 'telephone' in content['results'][h].keys():
            telephone = content['results'][h]['telephone']
        else:
            telephone = None
        if 'uid' in content['results'][h].keys():
            uid = content['results'][h]['uid']
        else:
            uid = None
        if 'street_id' in content['results'][h].keys():
            street_id = content['results'][h]['street_id']
        else:
            street_id = None
        if content['results'][h]['detail'] == 1:
            if 'type' in content['results'][h]['detail_info'].keys():
                type0 = content['results'][h]['detail_info']['type']
            else:
                type0 = None
            if 'tag' in content['results'][h]['detail_info'].keys():
                tag = content['results'][h]['detail_info']['tag']
            else:
                tag = None
        else:
            type0 = None
            tag = None

        if area == region[3:]:#区域相符才存数据
            try:
                sql = "insert into poi_full(keyword,name0,lng,lat,address,province,city,area,telephone,uid,street_id,type0,tag) " \
                      "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                data0 = (Key_word,name,lng,lat,address,province,city,area,telephone,uid,street_id,type0,tag)
                cursor.execute(sql % data0)
                connect.commit()
            except Exception as e:
                print(e)
        else:pass
    cursor.close()

if __name__ == "__main__":
   aks = get_ak()
   keyword = get_Keyword()
   region,lng_lat = get_Region()
   connect = mysql_Detail()
   get_Url(keyword, region, lng_lat,aks,connect)
   connect.close()
