from tkinter import *

import tkinter.simpledialog as dl
import tkinter.messagebox as mb

# tkinter GUI Input Output Example
# 设置GUI
root = Tk()
w = Label(root, text="Label Title")
w.pack()

# 欢迎消息
mb.showinfo("Welcome", "Welcome Message")
guess = dl.askinteger("Number", "Enter a number")

output = 'This is output message'
mb.showinfo("Output: ", output)


# Python OO example

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def introduce(self):
        print("hi! I'm " + self.name)
        print("my grade is: " + str(self.grade))

    def improve(self, amount):
        self.grade = self.grade + amount


jim = Student("jim", 86)
jim.introduce()

jim.improve(10)
jim.introduce()

# def add_candles(cake_func):
#     def insert_candles():
#         return cake_func() + " candles"
#     return insert_candles
#
# def make_cake():
#     return "cake"
#
# gift_func = add_candles(make_cake)
#
# print(make_cake())
# print(gift_func())


# def add_candles(cake_func):
#     def insert_candles():
#         return cake_func() + " candles"
#     return insert_candles
#
# def make_cake():
#     return "cake"
#
# make_cake = add_candles(make_cake)
#
# print(make_cake())
# # print(gift_func)


# def add_candles(cake_func):
#     def insert_candles():
#         return cake_func() + " and candles"
#     return insert_candles
#
# @add_candles
# def make_cake():
#     return "cake"
#
# # make_cake = add_candles(make_cake)
#
# print(make_cake())
# # print(gift_func)



some_sentences = '''\
I love learning python
because python is fun
and also easy to use
'''

#Open for 'w'irting
f = open('sentences.txt', 'w')
#Write text to File
f.write(some_sentences)
f.close()

#If not specifying mode, 'r'ead mode is default
f = open('sentences.txt')
while True:
    line = f.readline()
    #Zero length means End Of File
    if len(line) == 0:
        break
    print(line)
# close the File
f.close


str_1 = input("Enter a string: ")
str_2 = input("Enter another string: ")

print("str_1 is: " + str_1 + ". str_2 is :" + str_2)
print("str_1 is {} + str_2 is {}".format(str_1, str_2))






#break & continue example
# number = 59
#
# while True:
#     guess = int(input('Enter an integer : '))
#     if guess == number:
#         # New block starts here
#         break
#
#         # New block ends here
#     if guess < number:
#         # Another block
#         print('No, the number is higher than that, keep guessing')
#         continue
#         # You can do whatever you want in a block ...
#     else:
#         print('No, the number is a  lower than that, keep guessing')
#         continue
#         # you must have guessed > number to reach here
#
# print('Bingo! you guessed it right.')
# print('(but you do not win any prizes!)')
# print('Done')

#continue and pass difference

# a_list = [0, 1, 2]
#
# print("using continue:")
# for i in a_list:
#     if not i:
#         continue
#     print(i)
#
# print("using pass:")
# for i in a_list:
#     if not i:
#         pass
#     print(i)




#while example

# number = 59
# guess_flag = False
#
#
# while guess_flag == False:
#     guess = int(input('Enter an integer : '))
#     if guess == number:
#         # New block starts here
#         guess_flag = True
#
#         # New block ends here
#     elif guess < number:
#         # Another block
#         print('No, the number is higher than that, keep guessing')
#         # You can do whatever you want in a block ...
#     else:
#         print('No, the number is a  lower than that, keep guessing')
#         # you must have guessed > number to reach here
#
# print('Bingo! you guessed it right.')
# print('(but you do not win any prizes!)')
# print('Done')

#For example

number = 59
num_chances = 3
print("you have only 3 chances to guess")

for i in range(1, num_chances + 1):
    print("chance " + str(i))
    guess = int(input('Enter an integer : '))
    if guess == number:
        # New block starts here
        print('Bingo! you guessed it right.')
        print('(but you do not win any prizes!)')
        break

        # New block ends here
    elif guess < number:
        # Another block
        print('No, the number is higher than that, keep guessing, you have ' + str(num_chances - i) + ' chances left')
        # You can do whatever you want in a block ...
    else:
        print('No, the number is lower than that, keep guessing, you have ' + str(num_chances - i) + ' chances left')
        # you must have guessed > number to reach here


print('Done')



# #if statement example
#
# number = 59
# guess = int(input('Enter an integer : '))
#
# if guess == number:
#     # New block starts here
#     print('Bingo! you guessed it right.')
#     print('(but you do not win any prizes!)')
#     # New block ends here
# elif guess < number:
#     # Another block
#     print('No, the number is higher than that')
#     # You can do whatever you want in a block ...
# else:
#     print('No, the number is a  lower than that')
#     # you must have guessed > number to reach here
#
# print('Done')
# # This last statement is always executed,
# # after the if statement is executed.


#the for loop example

# for i in range(1, 10):
#     print(i)
# else:
#     print('The for loop is over')
#
#
# a_list = [1, 3, 5, 7, 9]
# for i in a_list:
#     print(i)
#
# a_tuple = (1, 3, 5, 7, 9)
# for i in a_tuple:
#     print(i)
#
# a_dict = {'Tom':'111', 'Jerry':'222', 'Cathy':'333'}
# for ele in a_dict:
#     print(ele)
#     print(a_dict[ele])
#
# for key, elem in a_dict.items():
#     print(key, elem)


# -*- coding: utf-8 -*-

# 默认参数
def repeat_str(s, times=1):
    repeated_strs = s * times
    return repeated_strs


repeated_strings = repeat_str("Happy Birthday!")
print(repeated_strings)

repeated_strings_2 = repeat_str("Happy Birthday!", 4)
print(repeated_strings_2)


# 不能在有默认参数后面跟随没有默认参数
# f(a, b =2)合法
# f(a = 2, b)非法

# 关键字参数: 调用函数时，选择性的传入部分参数
def func(a, b=4, c=8):
    print('a is', a, 'and b is', b, 'and c is', c)


func(13, 17)
func(125, c=24)
func(c=40, a=80)


# VarArgs参数
def print_paras(fpara, *nums, **words):
    print("fpara: " + str(fpara))
    print("nums: " + str(nums))
    print("words: " + str(words))


print_paras("hello", 1, 3, 5, 7, word="python", anohter_word="java")



# -*- coding: utf-8 -*-

#创建一个列表

number_list = [1, 3, 5, 7, 9]

string_list = ["abc", "bbc", "python"]

mixed_list = ['python', 'java', 3, 12]


#访问列表中的值

second_num = number_list[1]

third_string = string_list[2]

fourth_mix = mixed_list[3]

print("second_num: {0} third_string: {1} fourth_mix: {2}".format(second_num, third_string, fourth_mix))

#更新列表
print("number_list before: " + str(number_list))

number_list[1] = 30

print("number_list after: " + str(number_list))

#删除列表元素
print("mixed_list before delete: " + str(mixed_list))

del mixed_list[2]

print("mixed_list after delete: " + str(mixed_list))

#Python脚本语言

print(len([1,2,3])) #长度
print([1,2,3] + [4,5,6]) #组合
print(['Hello'] * 4) #重复
print(3 in [1,2,3]) #某元素是否在列表中

#列表的截取
abcd_list =['a', 'b', 'c', 'd']
print(abcd_list[1])
print(abcd_list[-2])
print(abcd_list[1:])

# 列表操作包含以下函数:
# 1、cmp(list1, list2)：比较两个列表的元素
# 2、len(list)：列表元素个数
# 3、max(list)：返回列表元素最大值
# 4、min(list)：返回列表元素最小值
# 5、list(seq)：将元组转换为列表
# 列表操作包含以下方法:
# 1、list.append(obj)：在列表末尾添加新的对象
# 2、list.count(obj)：统计某个元素在列表中出现的次数
# 3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
# 4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
# 5、list.insert(index, obj)：将对象插入列表
# 6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# 7、list.remove(obj)：移除列表中某个值的第一个匹配项
# 8、list.reverse()：反向列表中元素
# 9、list.sort([func])：对原列表进行排序



# 列表操作包含以下函数:
# 1、cmp(list1, list2)：比较两个列表的元素
# 2、len(list)：列表元素个数
# 3、max(list)：返回列表元素最大值
# 4、min(list)：返回列表元素最小值
# 5、list(seq)：将元组转换为列表
# 列表操作包含以下方法:
# 1、list.append(obj)：在列表末尾添加新的对象
# 2、list.count(obj)：统计某个元素在列表中出现的次数
# 3、list.extend(seq)：在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
# 4、list.index(obj)：从列表中找出某个值第一个匹配项的索引位置
# 5、list.insert(index, obj)：将对象插入列表
# 6、list.pop(obj=list[-1])：移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
# 7、list.remove(obj)：移除列表中某个值的第一个匹配项
# 8、list.reverse()：反向列表中元素
# 9、list.sort([func])：对原列表进行排序


#创建只有一个元素的tuple，需要用逗号结尾消除歧义
a_tuple = (2,)

#tuple中的list
mixed_tuple = (1, 2, ['a', 'b'])

print("mixed_tuple: " + str(mixed_tuple))

mixed_tuple[2][0] = 'c'
mixed_tuple[2][1] = 'd'

print("mixed_tuple: " + str(mixed_tuple))



