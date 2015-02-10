#!/usr/bin/python
#-*- coding: utf-8 -*-

class Person(object):
	"""docstring for Person"""
	__slots__ = ('__name', '__age')
	def __init__(self, name, age):
		print 'Person __init__', name, age
		#super(Person, self).__init__()
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

	def __del__(self):
		print 'Person destruct!!!', self.__name

class Student(Person):
	"""docstring for Student"""
	def __init__(self, name, age, score):
		print 'Student __init__', name, age, score
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
		%(self.name, self.age, self.__score)

	def info(self):
		print '__dict__ = ', self.__dict__
		print '__doc__ =  ', self.__doc__
		print '__module__ = ', self.__module__

	def __str__(self):
		return 'Student(%s, %d, %d)' %(self.name, self.age, self.__score)

	def __del__(self):
		print 'Student destruct!!!', self.name

class coding(object):
	"""docstring for coding"""
	def __init__(self, code):
		print 'coding __init__', code
		#super(coding, self).__init__()
		self.__code = code

	def work(self):
		print 'I am coding by', self.__code

	def __del__(self):
		print 'coding destruct!!!', self.__code

class Employer(Person, coding):
	"""docstring for Employer"""
	def __init__(self, name, age, code, salary, phone, address):
		print 'Employer __init__', name, age, code, salary, phone, address
		#super(Employer, self).__init__(name, age, code)
		Person.__init__(self, name, age)
		coding.__init__(self, code)
		self.__salary = salary
		self.__phone = phone
		self.__address = address

	def infomation(self):
		print 'My name is', self.name
		print 'My age is', self.age
		print 'My salary is', self.__salary
		print 'My phone number is', self.__phone
		print 'My address is', self.__address
		self.work()

	def __del__(self):
		print 'Employer destruct!!!', self.name

	def setSalary(self, value):
		self.__salary = value

	def getSalary(self):
		return self.__salary

	salary = property(getSalary, setSalary)

	@staticmethod
	def staticMethod():
		print 'staticmethod test!'
		
def main():
	#Person
	p = Person('ZhangSan', 20)
	print p.name
	print p.age
	print p.say()
	p.name = 'LiShi'
	p.age = 32
	print p.name
	print p.age
	print p.say()
	#Student
	s = Student('Wanwu', 18, 80)
	print s.name
	print s.age
	print s.score
	s.say()
	s.name = 'ZhaoLiu'
	s.age = 16
	s.score = 99
	s.say()
	s.info()
	print dir(s)
	print s
	#Employer
	e = Employer('Lilei', 26, 'Python', 8000, '123456789', 'China')
	e.infomation()
	e.salary = 8888
	e.infomation()
	Employer.staticMethod()

if __name__ == '__main__':
	main()
		