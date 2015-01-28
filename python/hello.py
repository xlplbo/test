# hello.py
#!/usr/bin/python
#-*- coding: utf-8 -*-

#输出
print "hello python", "can not use chinese", "realy?", "continue"

#输入
#name = raw_input("please input your name:")
#print name
#print type(name)

#代码段缩进
a = 100
if a > 1000 :
	print a
else : 
	print -a

#变量
a = "abc"
b = a
a = "XYZ"
print a, b

#list
classmates = ['zhangsan', 'lisi', 'wangwu']
print classmates
print classmates[0]
print classmates[1]
print classmates[2]
print classmates[-1]
print classmates[-2]
print classmates[-3]
classmates.append('liulu')
classmates.insert(0, 'zhaoqi')
print classmates
classmates.pop()
classmates.pop(0)
print classmates
classmates[0] = 'who?'
print classmates
classmates[-1] = ['wangwu1', 'wangwu2', 'wangwu3']
print classmates

#tuple
classmates2 = ('zhangsan', 'lisi', 'wangwu')
print classmates2
print classmates2[0]
print classmates2[-1]

#()不同含义
t = (1)
print type(t)
t2 = (1,)
print type(t2)

#tuple内嵌套list，可变的tuple
mulclassmates = (1, 'haha', ['why', 'can', 'become'])
print mulclassmates
mulclassmates[-1].append('append')
print mulclassmates

#条件语句分支
age = 3
if (age >= 18):
	print 'your age is', age
	print 'adult'
elif (age >= 6):
	print 'your age is', age
	print 'teenager'	
#print 'test'
else:
	print 'your age is', age
	print 'kid'

#for循环
for var in mulclassmates:
	print var

#while循环	
n = len(mulclassmates)
while (n > 0): 
	print mulclassmates[n-1]
	n -= 1

#字典dict
dictionary = {"Michael":95, "Bob":75, "Tracy":85}
print dictionary["Michael"] 
print dictionary.get("zhangsan")
print "Michael" in dictionary

#集合set，支持交集并集
set1 = set([1, 2, 3])
set2 = set([2, 3, 4])
print set1 & set2
print set1 | set2

#函数定义
def myabs( x ):
	if x >= 0:
		return x
	else: 
		return -x
	return

#执行空操作
pass

print myabs(-100)
	
def myabs2( x ):
	if not isinstance(x, (int, float)):
		#raise TypeError("bad operand type")
		pass
	if x >= 0:
		return x
	else: 
		return -x
	return

print myabs2('test')
print myabs2(-123)

#函数多返回值，返回tuple
def testFunc( x ):
	if x > 0:
		return x, x*x
	else: 
		return x
	return
	
print type(testFunc(2))
print testFunc(2)
print type(testFunc(-2))
print testFunc(-2)

def hello():
	print "hello python"
	return
	
hello()

#函数默认参数
def power( x, n = 2 ):
	s = 1
	while (n > 0): 
		n -= 1
		s *= x
	return s
	
print power(5)
print power(5, 3)

#函数默认参数最好是不可变的
def add_end( l=[] ):
	l.append('END')
	print l
	return
	
add_end()
add_end()

def add_end2( l=None ):
	if l is None:
		l = []
	l.append('END')
	print l
	return
	
add_end2()
add_end2()

#函数可变参数
def calc( number ):
	sum = 0
	for n in number:
		sum += n*n
	return sum
	
def calc2( *number ):
	sum = 0
	for n in number:
		sum += n*n 
	return sum
	
nums = [1, 2, 3, 4, 5]
print calc(nums)
print calc2(1, 2, 3, 4, 5)
print calc2(*nums)

#函数关键字参数（可选参数）
def person( name, age, **kw ):
	print 'name:', name, 'age:', age, 'other:', kw
	return
	
person("Micheal", 30)
person("Micheal", 30, city='beijing')
person("Micheal", 30, genger='M', city='beijing')

#函数参数组合
#参数定义的顺序必须是：必选参数、默认参数、可变参数和关键字参数
def func(a, b, c=0, *args, **kw):
    print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw

#递归函数
def fact( n ):
	if n == 1:
		return 1
	return n * fact(n-1)
	
print fact(10)


