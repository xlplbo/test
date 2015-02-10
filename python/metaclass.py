#!/usr/bin/python
#-*- coding: utf-8 -*-

class Field(object):
	"""docstring for Field"""
	def __init__(self, name, colum_type):
		super(Field, self).__init__()
		self.name = name
		self.colum_type = colum_type
	def __str__(self):
		return '<%s:%s>' %(self.__class__.__name__, self.name)
		
class StringField(Field):
	"""docstring for StringField"""
	def __init__(self, name):
		super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
	"""docstring for IntegerField"""
	def __init__(self, name):
		super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):
	"""docstring for ModelMetaclass"""
	def __new__(cls, name, bases, attrs):
		print 'ModelMetaclass', cls, name, bases, attrs
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		print 'Found model:%s' %name
		mappings = dict()
		for k, v in attrs.iteritems():
			if isinstance(v, Field):
				print 'Found mappings: %s ==> %s' %(k, v)
				mappings[k] = v
		for k in mappings.iterkeys():
			attrs.pop(k)	
		attrs['__mappings__'] = mappings
		attrs['__table__'] = name
		return type.__new__(cls, name, bases, attrs)					

class Model(dict):
	"""docstring for Model"""
	__metaclass__ = ModelMetaclass

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r'"Model" object has no attribute' %key)
	
	def __setattr__(self, key, value):
		self[key] = value

	def save(self):
		field = []
		params = []
		args = []
		for k, v in self.__mappings__.iteritems():
			field.append(v.name)
			params.append('?')
			args.append(getattr(self, k, None))
		sql = 'insert into %s (%s) values (%s)' %(self.__table__, ','.join(field), ','.join(params))
		print 'Sql: %s' %sql
		print 'ARGS: %s' %str(args)
		
class User(Model):
	"""docstring for User"""
	def __init__(self, **kw):
		super(User, self).__init__(**kw)

	id = IntegerField('uid')
	name = StringField('username')
	email = StringField('email')
	password = StringField('password')
		
def main():
	#“Object Relational Mapping”，即对象-关系映射
	u = User(id='123456', name='Mick', email='mick@gmail.com', password='12345678')
	u.save()

if __name__ == '__main__':
	main()
		