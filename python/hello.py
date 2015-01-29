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

#切片(前闭后开区间)
mylist = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
print mylist[1:3]
print mylist[-3:-1]

#迭代
for k, v in dictionary.iteritems():
	print k, v

#是否可迭代
from collections import Iterable
print isinstance(dictionary, Iterable)

#列表生成式
list_comp = [x * x for x in range(1, 11) if x % 2 == 0]
print list_comp
list_comp = [m + n for m in 'ABC' for n in 'XYZ']
print list_comp
import os
print [d for d in os.listdir('.')]
dictionary1 = {'x':'A', 'y':'B', 'z':'C'}
print [k + '=' + v for k, v in dictionary1.iteritems()]
list1 = ['Hello', 'World', 'KING', 'Apple', 18, (1, 2, 3)]
print [s.lower() for s in list1 if isinstance(s, str)]

#生成器
genertor = (x*x for x in range(10))
print genertor.next()
print genertor.next()

def fib(max):
	n, a, b = 0, 0, 1
	while  n < max:
		yield b
		a, b = b, a + b
		n += 1
print fib(6)
print fib(6).next()
for m in fib(6):
	print m

def odd():
	print 'step 1'
	yield 1
	print 'step 2'
	yield 2
	print 'step 3'
	yield 3

for n in odd():
	print n

#高阶函数
def add(a, b, func):
	return func(a) + func(b)

print add(-1, -3, abs)

#map()函数接收两个参数，一个是函数，一个是序列，map将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回
def function1(x):
	return x*x

print map(function1, [1, 2, 3, 4, 5, 6])

def fn1(s):
	return map(lambda sz: sz[0].upper() + sz[1:].lower(), s)

print fn1(['ASIiaA', 'Swwa', 'aSWVsA'])

#reduce把一个函数作用在一个序列[x1, x2, x3...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
def function2(x, y):
	return x*10 + y

print reduce(function2, [1, 2, 3, 4, 5, 6])

def prod(l):
	return reduce(lambda x, y: x * y, l)
print prod([1, 2, 3, 4, 5])

def str2int(s):
	def fn(x, y):
		return x*10 + y
	def char2num(s):
		return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
	return reduce(fn, map(char2num, s))

print str2int('123456789') + 1
#print char2num('2') undefine

#filter函数用于过滤序列
#filter()也接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
import math
def isprime(x):
	if type(x) != int:
		return False
	if x <= 1:
		return False
	if x == 2 or x == 3 or x == 5 or x ==7:
		return True
	if x%2 == 0 or x%3 == 0 or x%5 == 0 or x%7 == 0:
		return False
	for a in range(8, int(math.sqrt(x))):
		if x % a == 0:
			return False
	return True

print filter(isprime, range(1, 100))

#sorted排序
def cmp_func(s1, s2):
	if s1 > s2:
		return 1
	if s1 < s2:
		return -1
	return 0;
print sorted([2, 6, 1, 8, 5, 6, 7, 9])
print sorted([2, 6, 1, 8, 5, 6, 7, 9], reverse=True)
print sorted(['about', 'Bob', 'Apple', 'zoo'], cmp_func)

#函数作为返回值
def lazy_sum(*args):
	def sum():
		ax = 0;
		for n in args:
			ax += n
		return ax
	return sum

f = lazy_sum(*range(1, 100))
print f()

#闭包
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs
#返回时在引用局部变量i
#返回函数不要引用任何循环变量，或者后续会发生变化的变量。
f1, f2, f3 = count()
print f1()
print f2()
print f3()

#匿名函数lambda
#匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
f = lambda x: x * x
print f(12)

#装饰器
def log(func):
	def  wrapper(*args, **kw):
		print 'call %s()...' % func.__name__
		return func(*args, **kw)
	return wrapper

#@语法把装饰器至于函数定义处
@log
def now():
	print 'now = log(now)'

now()

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s %s()...:' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute')
def now():
    print 'now = log(now)'

now()

def log(func):
    def wrapper(*args,**kw):
        print 'begin call %s():' %func.__name__
        func(*args,**kw)
        print 'end call %s():' %func.__name__
    return wrapper

@log
def now():
    print '2013-12-25'

now()


#偏函数
import functools
print int('123')
int2 = functools.partial(int, base=2)
print int2('0110')



