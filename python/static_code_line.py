#!/usr/bin/python
#-*- coding: utf-8 -*-

import os

result = {}
def static(path = '.'):
	if os.path.isdir(path):
		for  x in os.listdir(path):
			childdir = os.path.join(path, x)
			if os.path.isdir(childdir):
				static(childdir)
			elif os.path.isfile(childdir):
				clacFilelines(childdir)
	elif os.path.isfile(path):
		clacFilelines(path)
	return

def clacFilelines(filepath):
	vpath = os.path.splitext(filepath)
	ext = vpath[1].lower()
	if not ext.strip():
		return False
	if not isTextFile(ext):
		return False
	lines = 0
	with open(filepath, 'rU') as f:
		filelist = f.readlines()
		for line in filelist:
			if not line.strip():
				continue	
			lines += 1
		if ext in result:
			result[ext] += lines
		else:
			result[ext] = lines
	print 'file:%s lines:%d' %(filepath, lines)
	return True

def isTextFile(ext):
	tExt = ('.c', '.cpp', '.h', '.py', '.htm', '.html', '.txt', '.lua', '.ini', '.hpp', '.lua', '.cfg')
	if ext in tExt:
		return True
	return False

if __name__ == '__main__':
	print '***********start code line static*************'
	static()
	print '****************static rezult*****************'
	sum = 0
	for k,v in result.iteritems():
		sum += v
		print '[%s]: %d lines' %(k, v)
	print 'total: %d lines' %sum
	print '******************static end******************'
