# hello.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "hello python", "can not use chinese", "realy?", "continue"

#name = raw_input("please input your name:")
#print name
#print type(name)

a = 100
if a > 1000 :
	print a
else : 
	print -a


a = "abc"
b = a
a = "XYZ"
print a, b

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

classmates2 = ('zhangsan', 'lisi', 'wangwu')
print classmates2
print classmates2[0]
print classmates2[-1]

t = (1)
print type(t)
t2 = (1,)
print type(t2)

mulclassmates = (1, 'haha', ['why', 'can', 'become'])
print mulclassmates
mulclassmates[-1].append('append')
print mulclassmates

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
	
for var in mulclassmates:
	print var
	
n = len(mulclassmates)
while (n > 0): 
	print mulclassmates[n-1]
	n -= 1
	
