#!/usr/bin/python
# coding:utf-8
# Contributor:
# 	liubo5 <lboxlp@163.com>

__version__ = '1.0'

import os
import sys
from optparse import OptionParser
import zipfile
import ConfigParser
import logging

RC_LOG_FILE = "autoconfig.log"
RC_CONFIG_FILE = "config.ini"
RC_WINDOW_PACK = "library.zip"
RC_COMMON_PACK = "data.zip" 
RC_EXT_OR_ELF = ('.dll', '.exe', ".so", ".a", 'kg_goddess', 'kg_bishop', 'so2relay', 'so2gamesvr')

class AutoConfig(object):
	"""docstring for AutoConfig"""
	def __init__(self, config, log):
		super(AutoConfig, self).__init__()
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.read(config)
		self.log = logging.getLogger(__file__)
		self.log.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		fh = logging.FileHandler(log, 'w')
		fh.setFormatter(formatter)
		self.log.addHandler(fh)
		sh = logging.StreamHandler()
		sh.setFormatter(formatter)
		self.log.addHandler(sh)

	def _isWondows(self):
		return sys.platform == 'win32'

	def _isLinux(self):
		return sys.platform.startswith('linux')

	def _checkFileExist(self, filename):
		for file in os.listdir("."):
			if os.path.isfile(file) and file == filename:
				self.log.info("file '%s' is OK, continue..." %filename)
				return True
		self.log.warn("can not find file '%s'" %filename)
		return False

	def _checkYesOrNO(self, title):
		while True:
			ret = raw_input(title)
			if ret.lower() == 'n' or ret.lower() == 'no':
				return False
			elif ret.lower() == 'y' or ret.lower() == 'yes':
				return True
			else:
				title = "please input(y/N) again:"

	def _isProgramsAndLibrary(self, file):
		vpath1 = os.path.splitext(file)
		ext1 = vpath1[1].lower()
		if ext1 in RC_EXT_OR_ELF:
			return True
		vpath2 = os.path.split(file)
		ext2 = vpath2[1].lower()
		if ext2 in RC_EXT_OR_ELF:
			return True
		if ext2[:len(ext2)-1] in RC_EXT_OR_ELF:
			return True
		return False

	def _getProgramsAndLibrary(self, path, filedict):	
		for x in os.listdir(path):
			childdir = os.path.join(path, x)
			if os.path.isdir(childdir):
				self._getProgramsAndLibrary(childdir, filedict)
			else:
				if self._isProgramsAndLibrary(x):
					filedict[x] = childdir

	def packLibrary(self, name):
		self.log.info("Prepare to packaged programs and librarys!")
		self.log.warn("please compile your project at first, and then run packaged program!")
		if self._checkFileExist(name):
			if self._checkYesOrNO("check file '%s' is exist! do you update this file?(y/N)" %name):
				self.log.info("remove '%s' ..." %name)
				os.remove(name)
			else:
				self.log.info("packaged finish! thanks all")
				return True
		filedict = {}
		path = self.configParser.get("packlibrary", "path")
		pathlist = path.split(',')
		for pathlv in pathlist:
			pathlv = pathlv.strip()
			if len(pathlv) <= 0:
				continue
			if not os.path.isdir(pathlv):
				self.log.error("packlibrary path '%s' is wrong, please check '%s'" %(pathlv, self.config))
				continue
			self.log.info("traverse '%s' directory ..." %pathlv)
			self._getProgramsAndLibrary(pathlv, filedict)
		if len(filedict) <= 0:
			self.log.error("can not find any program or library, please build project and run again")
			return False
		zipFile = zipfile.ZipFile(name, 'a', zipfile.ZIP_DEFLATED)
		for k, v in filedict.iteritems():
			self.log.info("file '%s' packaged" %k)
			zipFile.write(v, k)
		zipFile.close()
		self.log.info("generate '%s' success! " %name)
		self.log.info("packaged programs and librarys finished!")

	def configClient(self):
		pass

	def configServer(self):
		pass

def main():
	#check python version
	if sys.version_info[0] > 2:
		print("The python version is %d.%d. But python 2.x is required. (Version 2.7 is well tested)\n"
			"Download it here: https://www.python.org/" % (sys.version_info[0], sys.version_info[1]))
		raw_input("\nplease input any key exit...")
		return False

	#check parameters type
	parser = OptionParser(usage="%%prog [-p|-c|-s|-h]\nnotice: please configurate [%s] at first" %RC_CONFIG_FILE)
	parser.add_option(
		"-p", "--packlibrary", action="store_false", dest="p", help="jv2 program and runtime librarys packaged")
	parser.add_option(
		"-c", "--client", action="store_false", dest="c", help="jv2 client automatic configuration")
	parser.add_option(
		"-s", "--server", action="store_false", dest="s", help="jv2 server automatic configuration")
	opts, args = parser.parse_args()
	if opts.p == None and opts.c == None and opts.s == None:
		parser.print_help()
		return False
	# if opts.p == False and opts.c == False:
	# 	parser.error("option -p and -c are mutually exclusive")
	# 	return False
	# if opts.p == False and opts.s == False:
	# 	parser.error("option -p and -s are mutually exclusive")
	# 	return False
	# if opts.c == False and opts.c == False:
	# 	parser.error("option -c and -c are mutually exclusive")
	# 	return False

	#execute
	config = AutoConfig(RC_CONFIG_FILE, RC_LOG_FILE)
	if opts.p != None:
		config.packLibrary(RC_COMMON_PACK)
	if opts.c != None:
		config.configClient()
	if opts.s != None:
		config.configServer()

	raw_input("\nplease input any key exit...")

if __name__ == '__main__':
	main()