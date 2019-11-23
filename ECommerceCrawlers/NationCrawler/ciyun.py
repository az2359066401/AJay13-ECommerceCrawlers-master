# -*- encoding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup  # 导入urllib库的request模块
import lxml  # 文档解析器
import time  # 时间模块
import os  # os模块就是对操作系统进行操作
import matplotlib.pyplot as plt  # 数学绘图库
import jieba  # 分词库
from PIL import Image  # 图片
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
from collections import Counter  # 列表、字典、字符串等中计算元素重复的次数
import numpy as np  # 科学计算

t = time.localtime(time.time())  # 转换至当前时区；time.time()：返回当前时间的时间戳；

foldername = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + str(
    t.__getattribute__("tm_mday")) + "-" + str(t.__getattribute__("tm_hour"))

picpath = './%s' % (foldername)


def txt(name, text):  # 定义函数名
    if not os.path.exists(picpath):  # 路径不存在时创建一个
        os.makedirs(picpath)
    savepath = picpath + '/' + name + '.txt'
    file = open(savepath, 'a', encoding='utf-8')
    file.write(text)
    # print(text)
    file.close
    return (picpath)


def get_text(bs):
    # 读取纯文本
    for p in bs.select('p'):
        t = p.get_text()
        # print(t)#输出文本
        txt('url2', t)


def FenCi(pathin, pathout1, pathout2, picturein, pictureout):
    text = open(pathin, "r", encoding='utf-8').read()  # 1、读入txt文本数据

    # 2、结巴分词，默认精确模式。可以添加自定义词典userdict.txt,然后jieba.load_userdict(file_name) ,file_name为文件类对象或自定义词典的路径
    # 自定义词典格式和默认词库dict.txt一样，一个词占一行：每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒
    cut_text = jieba.cut(text, cut_all=False)
    result = " ".join(cut_text)
    # print(result)
    with open(pathout1, 'a', encoding='utf-8') as f:
        f.write(result)
    print("save")

    # 3、wordcount
    with open(pathout1, 'r', encoding='utf-8') as fr:  # r:只读；w:只写
        data = jieba.cut(fr.read())
    data = dict(Counter(data))

    with open(pathout2, 'a', encoding='utf-8') as fw:  # 读入存储wordcount的文件路径
        for k, v in data.items():
            fw.write('%s,%d\n' % (k, v))

    # 4、初始化自定义背景图片
    image = Image.open(picturein)
    graph = np.array(image)

    # 5、产生词云图
    # 有自定义背景图：生成词云图由自定义背景图像素大小决定
    wc = WordCloud(font_path=r"C://Windows/Fonts/Courier New/simsun.ttc", background_color='white', max_font_size=50,
                   mask=graph)
    wc.generate(result)

    # 6、绘制文字的颜色以背景图颜色为参考
    image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
    wc.recolor(color_func=image_color)
    wc.to_file(pictureout)


def readhtml(path):  # 读取网页文本
    res = urllib.request.urlopen(path)  # 调用urlopen()从服务器获取网页响应(respone)，其返回的响应是一个实例
    html = res.read().decode('utf-8')  # 调用返回响应示例中的read()，可以读取html
    soupa = BeautifulSoup(html, 'lxml')
    result = soupa.find_all('div', class_='result')
    download_soup = BeautifulSoup(str(result), 'lxml')  # 使用查询结果再创建一个BeautifulSoup对象,对其继续进行解析

    urls = []
    url_all = download_soup.find_all('a')
    # 抓取所有政策链接
    for a_url in url_all:
        a_url = a_url.get('href')
        urls.append(a_url)
        if a_url and a_url.startswith('http'):
            url = a_url
            txt('url0', a_url)
            # res = urllib.request.Request(url)# 指定要抓取的网页url
            try:
                res = urllib.request.urlopen(url)
            except Exception:
                continue
            if res.getcode() == 200:
                html = res.read().decode('utf-8')
                # html = urllib.request.urlopen(res).read().decode("UTF-8")

                # print(html)
                txt('url1', html)
                soup = BeautifulSoup(html, 'lxml')
                get_text(soup)


for n in range(3):
    url = r'http://sousuo.gov.cn/s.htm?t=govall&advance=false&n=10&p=' + str(
        n) + '&timetype=&mintime=&maxtime=&sort=&q=%E5%A4%A7%E6%95%B0%E6%8D%AE'
    # url = r'http://sousuo.gov.cn/s.htm?q=&n=10&p=' + str(n) + '&t=paper&advance=true&title=%E5%85%BB%E8%80%81&content=&puborg=&pcodeJiguan=&pcodeYear=&pcodeNum=&childtype=&subchildtype=&filetype=&timetype=timeqb&mintime=&maxtime=&sort=&sortType=1&nocorrect='  # 指定要抓取的网页url，必须以http开头
    readhtml(url)
# picpath + '\\url2.txt'
a = picpath + './url2.txt'
b = picpath + './result.txt'
c = picpath + './result.csv'
d = r'./1.jpg'
e = picpath + './wordcloud.png'
FenCi(a, b, c, d, e)
print('finish')
