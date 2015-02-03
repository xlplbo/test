#!/usr/bin/python
#-*- coding: utf-8 -*-
#序列化

try:
	import cPickle as pickle
except ImportError:
	import pickle

d = dict(name='Bob', age=20, score=80)
print pickle.dumps(d)

import json
print json.dumps(d)