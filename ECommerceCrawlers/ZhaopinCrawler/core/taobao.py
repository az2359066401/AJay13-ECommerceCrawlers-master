from selenium import webdriver
from selenium.webdriver.common.by import By  #查找元素的方法，此次用于搜索框查找
from selenium.webdriver.support.ui import WebDriverWait #显示等待，设置最长等待时间，此次用于打开链接的最长等待时间

from selenium.webdriver.support import expected_conditions as EC #EC.presence_of_element_located（）是确认元素是否已经出现了或者可点击等
from selenium.common.exceptions import TimeoutException #异常处理,try exceptions
from pyquery import PyQuery as pq  #基于前端的解析代码的工具
import re  #正则表达式
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys

client = MongoClient()
db = client.taobao
yurongfu = db.yurongfu #创建羽绒服集合

driver = webdriver.Chrome() #打开Chrome浏览器,C要大写
wait = WebDriverWait(driver,10) #设置浏览器等待时间

#进入淘宝网，输入鞋子，返回页面
def search():
    try:
        driver.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))) #定位输入框
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))) #定位搜索按钮
        input.send_keys(u'羽绒服') #输入羽绒服
        submit.click() #模拟提交按钮
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))) #确保所有页数信息加载完毕
        get_products() #调用得到所有产品函数
        return total.text
    except TimeoutException:
        return search()

#跳转到下一页
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))) #相当于input这个页码输入框输入了page_number
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))) #定位确定按钮
        input.clear() #clear() 函数用于删除字典内所有元素
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number))) #某个元素文本包含某文字
        get_products()
    except TimeoutException:
        next_page(page_number)

#得到淘宝商品信息
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = driver.page_source
    doc = pq(html)
    #pyquery （driver.page_source）就相当于requests.get获取的内容
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),#用这个类代表这个标签
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        yurongfu.insert(product)

def main():  #定义主函数
    total = search()
    total= int(re.compile('(\d+)').search(total).group(1))
        #爬取所有的数据时，把10替换为total+1
    for i in range(1,10):
        next_page(i)

if __name__ == '__main__':
    main()
