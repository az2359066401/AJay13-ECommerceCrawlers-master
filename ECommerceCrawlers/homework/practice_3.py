#coding=utf-8
#@description:周末作业

#一.已经字符串 s = "i,am,lilei",请用两种办法取出之间的“am”字符。
print('第一题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

#方法1
s = "i,am,lilei"
print(s[2:4])
##方法2
c = s.split(',')[1]
print(c)

print('第二题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

#二.在python中，如何修改字符串？

#答案：可以用字符串的replace方法.
ainfo = 'i love php'
replycontent = ainfo.replace('php','python')
print(replycontent)

print('第三题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

#三.bool("2012" == 2012) 的结果是什么。

##答案：结果是fasle,==判断对象的数据类型，尽管看起来数值是一样的，但是他们的类型不同，一个是字符串，一个是数字


print('第四题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

##四.已知一个文件 test.txt，内容如下：

f = open('test.txt','rb')
content = f.read()
dcontent = content.decode('utf-8')##转换为unicode

##1.请输出内容
print(dcontent)

##2.请计算该文本的原始长度.
print(len(dcontent))

##3.请去除该文本的换行
print(dcontent.replace('\n',''))

##4.请替换其中的字符"2012"为"2013"。
print(dcontent.replace('2012','2013'))

##5.请取出最中间的长度为5的子串。
print(dcontent[int(len(dcontent)/2):int(len(dcontent)/2)+5].encode('utf-8'))
##6.请取出最后2个字符。
print('aaaa--------')
print(dcontent[-2:].encode('utf-8'))
print('bbbb--------')
##7.请从字符串的最初开始，截断该字符串，使其长度为11.
print(dcontent[:11].encode('utf-8'))

##8.请将{4}中的字符串保存为test1.py文本.

rinfo = dcontent.replace('2012','2013')
f = open('test1.py','w')
f.write(rinfo)
f.close()##关闭文件

print('第五题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

##五.请用代码的形式描述python的引用机制。

import sys

cinfo = '1234'
print(id(cinfo))
print(sys.getrefcount('1234')   )

binfo = '1234'
print(id(binfo))
print(sys.getrefcount('1234'))

print('第六题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')

##六.已知如下代码

a = "中文编程"  ##引用计数开始是3，然后a变量引用了字符串对象3 + 1 =4
print("a:%s" % id(a))

b = a
print("b:%s" % id(b))##4 + 1 = 5

c = a
print("c:%s" % id(c))## 5 + 1 = 6

print(sys.getrefcount('中文编程'))##输出结果是6
print('ssss')
a = "python编程"
print("a:%s" % id(a))###6-1 = 5##a引用另外一个字符串对象

b = u'%s' % bytes(a, 'utf-8').decode('utf-8')
print("b:%s" % id(b))###5-1 = 4

print(sys.getrefcount('中文编程'))##输出结果是4

d = "中文编程"
print("d:%s" % id(d))###新建一个变量，引用字符串 4 + 1 = 5

e = a
print("e:%s" % id(e))

c = b
print("c:%s" % id(c))### c引用另外一个字符串对象，5 - 1 = 4

print(sys.getrefcount('中文编程'))


b2 = a.replace("中","中")
print("b2:%s" % id(b2))

print('result-----------------')
print(sys.getrefcount('中文编程'))
print(sys.getrefcount('python编程'))


print('第七题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')
##七.已知如下变量

a = "字符串拼接1"
b = "字符串拼接2"
#
##请用四种以上的方式将a与b拼接成字符串c。并指出每一种方法的优劣

##方法1：在做大量的字符串对象拼接的时候不推荐

c = a + b

##方法2：

c = "%s%s" % (a,b)

###方法3：
print('format')
c = "{a}{b}" .format (a=a,b=b)


##方法4：

c = "".join([a,b])

print(c)


##请将a与b拼接成字符串c，并用逗号分隔。

c = '%s,%s' % (a,b)

##.请计算出新拼接出来的字符串长度，并取出其中的第七个字符。
lennum = len(c.decode('utf-8'))
print(c.decode('utf-8')[6].encode('utf-8'))

print('第八题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')
##八.请阅读string模块，并且，根据string模块的内置方法输出如下几题的答案
import string
##1.包含0-9的数字。

#print(help(string)
print(string.digits)

##2.所有小写字母
print(string.lowercase)

##3.所有标点符号
print(string.punctuation)

##4:所有大写字母和小写字母。
print(string.ascii_lowercase)##小写字母
print(string.ascii_uppercase)##大写字母
print('\n')
##5：请使用你认为最好的办法将{1}-{4}点中的字符串拼接成一个字符串。
strinfo = []
strinfo.append(string.digits)
strinfo.append(string.lowercase)
strinfo.append(string.punctuation)
strinfo.append(string.ascii_lowercase)
strinfo.append(string.ascii_uppercase)
print("".join(strinfo))
print('\n')
strinfo = "%s%s%s%s%s" % (string.digits,string.lowercase,string.punctuation,string.ascii_lowercase,string.ascii_uppercase)
print(strinfo)



print('第九题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')
##九.已知字符串

a = "i,am,a,boy,in,china"

##1.假设boy和china是随时可能变换的，例boy可能改成girl或者gay，而china可能会改成别的国家，你会如何将上面的字符串，变为可配置的。

ac = "i,am,a,%(sex)s,in,%(country)s"  % {'sex':'girl','country':'china'}
bc = "i,am,a,{sex},in,{country}" .format (sex='girl',country='india')
print(ac)
print(bc)

##2.请使用2种办法取出其间的字符"boy"和"china"。

##方法1
print(a[7:10])
print(a[-5:])

##方法2
cinfo = a.split(',')
print(cinfo[3])
print(cinfo[-1])

##3.请找出第一个"i"出现的位置。

print(a.find('i'))##-1
print(a.index('i'))##报错

##4.请找出"china"中的"i"字符在字符串a中的位置。
print(a.find('i',a.find('china')))
print(a.rfind('i'))

##5.请计算该字符串一共有几个逗号
print(a.count(','))

print('第十题－－－－－－－－－－－－－－－－－－－－－－－－－－－－－')
##十.请将模块string的帮助文档保存为一个文件。

import sys
import string

f = open('test.log','w')
sys.stdout = f
help(string)
f.close()
