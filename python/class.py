#!/usr/bin/python
#-*- coding: utf-8 -*-

class Person(object):
	"""docstring for Person"""
	__slots__ = ('__name', '__age')
	def __init__(self, name, age):
		super(Person, self).__init__()
		self.__name = name
		self.__age = age

	@property
	def name(self):
		return self.__name
	@name.setter
	def name(self, value):
		self.__name = value

	@property
	def age(self):
		return self.__age
	@age.setter
	def age(self, value):
		self.__age = value

	def say(self):
		print 'Hello, My Name is %s, My age is %d' %(self.__name, self.__age) 

p = Person('ZhangSan', 20)
print p.name
print p.age
print p.say()
p.name = 'LiShi'
p.age = 32
print p.name
print p.age
print p.say()

class Student(Person):
	"""docstring for Student"""
	def __init__(self, name, age, score):
		super(Student, self).__init__(name, age)
		self.__score = score

	@property
	def score(self):
		return self.__score
	@score.setter
	def score(self, value):
		self.__score = value

	def say(self):
		print 'Hello, I am a Student, My Name is %s, My age is %d, My score is %d' \
		%(super(Student, self).name, super(Student, self).age, self.__score)

s = Student('Wanwu', 18, 80)
print s.name
print s.age
print s.score
s.say()
s.name = 'ZhaoLiu'
s.age = 16
s.score = 99
s.say()