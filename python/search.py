#!/usr/bin/python
#-*- coding: utf-8 -*-
#搜索目录

import os

def search(d = '.', f = 0):
	if os.path.isdir(d):
		for  x in os.listdir(d):
			childdir = os.path.join(d, x)
			if os.path.isdir(childdir):
				print '[ dir]', f, childdir
				search(childdir, f+1)
			elif os.path.isfile(childdir):
				print '[file]', f, childdir
	elif os.path.isfile(d):
		print '[file]', f, d
	return

print 'PATH:'
search('C:/Users/liubo5/Desktop/test/')