#!/usr/bin/python
#-*- coding: utf-8 -*-

#字符反转
astring = 'abcdefg hijk'
print astring[::-1]
print ' '.join(astring[::-1])

#逐词反转
import re
atext = 'who are you'
print ' '.join(re.split(r'\s+', atext)[::-1])
print ' '.join(reversed(re.split(r'\s+', atext)))

