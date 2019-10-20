#encoding=utf-8
#@description:周末习题

##习题1：

#列表a = [11,22,24,29,30,32]

a = [11,22,24,29,30,32]

#1 把28插入到列表的末端

a.append(28)


#2 在元素29后面插入元素57

a.insert(4,57)


#3 把元素11修改成6

a[0] = 6

#3 删除元素32

##如果是用a列表用上面已经操作过的数据：a = [6,22,24,29,57,30,32,28]答案是：
##方法1
a.pop(-2)

##方法2
del a[-2]

##如果a列表:a = [11,22,24,29,30,32] 用原来的数据，答案是：

##方法1
a.pop(-1)

##方法2
del a[-1]


#4 对列表从小到大排序

a.sort()


##习题2：

##列表b = [1,2,3,4,5]

b = [1,2,3,4,5]

#1 用2种方法输出下面的结果：

#[1,2,3,4,5,6,7,8]

##方法1:

c = b + [6,7,8]

##方法2

b.extend([6,7,8])


##2 用列表的2种方法返回结果：[5,4]

##方法1：

b = [1,2,3,4,5]

print(b[-1:-3:-1])

##方法2：
c = []
c.append(b.pop())
c.append(b.pop())
print(c)

##3 判断2是否在列表里

if 2 in b:
    print('2 in b')


##习题3：

b = [23,45,22,44,25,66,78]

##用列表解析完成下面习题：

##1 生成所有奇数组成的列表

print( [m for m in b if m % 2 == 1])

##2 输出结果: ['the content 23','the content 45']

print(['the content %s ' % m for m in b[:2]])

##3 输出结果: [25, 47, 24, 46, 27, 68, 80]

print([m + 2 for m in b])


##习题4：

##用range方法和列表推导的方法生成列表：

##[11,22,33]

##range方法

print(range(11,34,11))

##列表推导

print([m * 11 for m in range(1,4)])

##习题5：

##已知元组:a = (1,4,5,6,7)

a = (1,4,5,6,7)

##1 判断元素4是否在元组里

print(4 in a)


##2 把元素5修改成8

b = list(a)
b[2] = 8
print(tuple(b))

##习题6：

##已知集合:setinfo = set('acbdfem')和集合finfo = set('sabcdef')完成下面操作：

setinfo = set('acbdfem')

finfo = set('sabcdef')


##1 添加字符串对象'abc'到集合setinfo

setinfo.add('abc')

##2 删除集合setinfo里面的成员m

setinfo.remove('m')

##3 求2个集合的交集和并集

##交集

setinfo & finfo

##并集

setinfo | finfo


##习题7：用字典的方式完成下面一个小型的学生管理系统。

##1 学生有下面几个属性：姓名，年龄，考试分数包括：语文，数学，英语得分。

##比如定义2个同学：

##姓名：李明，年龄25，考试分数：语文80，数学75，英语85

##姓名：张强，年龄23，考试分数：语文75，数学82，英语78分


studentinfo = {'liming':{'name':'李明','age':25,'fenshu':{'chinese':80,'math':75,'english':85}}}

studentinfo['zhangqiang'] = {'name':'张强','age':23,'fenshu':{'chinese':75,'math':82,'english':78}}



##2 给学生添加一门python课程成绩，李明60分，张强：80分

studentinfo['liming']['fenshu']['python'] = 60
studentinfo['zhangqiang']['fenshu']['python'] = 80


##3 把张强的数学成绩由82分改成89分

studentinfo['zhangqiang']['fenshu']['math'] = 89


##4 删除李明的年龄数据

studentinfo['liming'].pop('age')


##5 对张强同学的课程分数按照从低到高排序输出。

binfo = studentinfo['zhangqiang']['fenshu'].values()
print(binfo)

##6 外部删除学生所在的城市属性，不存在返回字符串 beijing

print(studentinfo.pop('city','beijing'))