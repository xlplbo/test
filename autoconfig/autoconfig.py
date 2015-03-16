#!/usr/bin/python
# coding:utf-8
# Contributor:
# liubo5 <lboxlp@163.com>

__version__ = '1.0'

import os
import sys
from optparse import OptionParser
import zipfile
import codecs
import ConfigParser
import logging
import shutil
import stat
import chardet

RC_LOG_FILE = "autoconfig.log"
RC_CONFIG_FILE = "config.ini"
RC_WINDOW_PACK = "library.zip"
RC_COMMON_PACK = "data.zip" 
RC_EXT_OR_ELF = ('.dll', '.exe', ".so", ".a", 'kg_goddess', 'kg_bishop', 'so2relay', 'so2gamesvr')
RC_CLIENT_LIST = ('curl.exe', 'engine.dll', 'lualibdll.dll', 'represent3.dll', 'sound.dll', 'dumper.dll',
			'dumpreport.exe', 'verify_up2date.exe', 'so2game.exe', 'rainbow.dll')

class AutoConfig(object):
	"""docstring for AutoConfig"""
	def __init__(self, config, log):
		super(AutoConfig, self).__init__()
		self.config = config
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.readfp(codecs.open(config, "r", self._getFileCoding(config)))  
		self.log = logging.getLogger(__file__)
		self.log.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		fh = logging.FileHandler(log, 'w')
		fh.setFormatter(formatter)
		self.log.addHandler(fh)
		sh = logging.StreamHandler()
		formatter = logging.Formatter('%(levelname)s: %(message)s')
		sh.setFormatter(formatter)
		self.log.addHandler(sh)

	def _isWondows(self):
		return sys.platform == 'win32'

	def _isLinux(self):
		return sys.platform.startswith('linux')

	def _getFileCoding(self, filename):
		charset = None
		with file(filename, "r") as f:
			charset = chardet.detect(f.read())
		return charset['encoding']

	def _checkFileExist(self, filename):
		for v in os.listdir("."):
			if os.path.isfile(v) and v == filename:
				self.log.info("file '%s' is OK, continue..." %filename)
				return True
		self.log.warn("can not find '%s'" %filename)
		return False

	def _checkYesOrNO(self, title):
		while True:
			ret = raw_input(title)
			if ret.lower() == 'n' or ret.lower() == 'no':
				return False
			elif ret.lower() == 'y' or ret.lower() == 'yes':
				return True
			else:
				title = "please input again(y/N):"

	def _isProgramsAndLibrary(self, filename):
		vpath1 = os.path.splitext(filename)
		ext1 = vpath1[1].lower()
		if ext1 in RC_EXT_OR_ELF:
			return True
		vpath2 = os.path.split(filename)
		ext2 = vpath2[1].lower()
		if ext2 in RC_EXT_OR_ELF:
			return True
		if ext2[:len(ext2)-1] in RC_EXT_OR_ELF:
			return True
		return False

	def _getProgramsAndLibrary(self, path, filedict):
		if os.path.exists(path) and not os.path.isdir(path) and self._isProgramsAndLibrary(path):
			filedict[os.path.split(path)[1]] = path
			return 
		for x in os.listdir(path):
			childdir = os.path.join(path, x)
			if os.path.isdir(childdir):
				self._getProgramsAndLibrary(childdir, filedict)
			else:
				if self._isProgramsAndLibrary(x):
					filedict[x] = childdir
		return

	def packLibrary(self, name):
		self.log.info("================================================")
		self.log.info("prepare to packaged programs and librarys!")
		self.log.warn("please compile your project at first, and then run packaged program!")
		if self._checkFileExist(name):
			if self._checkYesOrNO("check file '%s' is exist! do you update this file?(y/N):" %name):
				self.log.info("remove '%s' ..." %name)
				os.chmod(name, stat.S_IREAD | stat.S_IWRITE)
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
				self.log.error("path '%s' is wrong, please check '%s'" %(pathlv, self.config))
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
		self.log.info("==> generate '%s' success! " %name)
		self.log.info("==> packaged programs and librarys finished!")

	def _getTreeDict(self, path, filedict):
		if os.path.exists(path) and not os.path.isdir(path):
			filedict[os.path.split(path)[1]] = path
			return
		for x in os.listdir(path):
			childdir = os.path.join(path, x)
			if os.path.isdir(childdir):
				self._getTreeDict(childdir, filedict) 
			else:
				filedict[x] = childdir
		return

	def _copyFile(self, srcname, dstname):
		try:
			if os.path.exists(dstname):
				if os.path.isdir(dstname):
					shutil.rmtree(dstname, False, self._handlerError)
				else:
					os.chmod(dstname, stat.S_IREAD | stat.S_IWRITE)
					os.remove(dstname)
			if os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isfile(srcname):
				shutil.copy2(srcname, dstname)
		except Exception, e:
			self.log.error(str(e))
		shutil.copystat(srcname, dstname)

	def _copyFolder(self, src, dst):
		if not os.path.exists(dst):
			os.mkdir(dst)
		for name in os.listdir(src):
			if '.svn' in name.strip():
				continue
			srcname = os.path.join(src, name)
			dstname = os.path.join(dst, name)
			if not os.path.isdir(srcname):
				self._copyFile(srcname, dstname)
			else:
				self._copyFolder(srcname, dstname)

	def _extractLibrary(self, path):
		self.log.info("copy windows librarys to '%s'" %path)
		zipFile = zipfile.ZipFile(RC_WINDOW_PACK, 'r', zipfile.ZIP_DEFLATED)
		for v in zipFile.namelist():
			zipFile.extract(v, path)
			self.log.info("extract '%s' ..." %v)

	def _extractFiles(self, path, list):
		self.log.info("copy programs and librarys to '%s'" %path)
		zipFile = zipfile.ZipFile(RC_COMMON_PACK, 'r', zipfile.ZIP_DEFLATED)
		extFile = []
		for v in zipFile.namelist():
			lfile = v.lower()
			lfiled = lfile.replace('d.', '.')
			if lfile in list and lfile not in extFile:
				zipFile.extract(v, path)
				extFile.append(lfile)
				self.log.info("extract '%s' ..." %v)
			elif lfiled in list and lfiled not in extFile:
				zipFile.extract(v, path)
				extFile.append(lfiled)
				self.log.info("extract '%s' ..." %v)
		for v in list:
			if v not in extFile:
				self.log.error("can not find '%s', please check '%s' file" %(v, RC_COMMON_PACK))

	def _handlerError(self, func, path, excinfo):
		os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
		func(path)
		self.log.info("Exception handling: %s %s" %(getattr(func, '__name__'), path))

	def _parseIniFile(self, filename, func, filedict, srcdir, catalog, dstdir):
		filepath = filedict.get(filename)
		if not filepath:
			self.log.error("can not find '%s'" %filename)
			return False
		for v in catalog:
			clv = os.path.join(srcdir, v)
			if clv in filepath:
				path = filepath.replace(clv, dstdir, 1)
				self.log.info("parser client '%s'" %path)
				if not os.path.isfile(path):
					self.log.error("parser client '%s' failed!" %path)
					return False
				func(path)
				lines = []
				with file(path, "r") as f:
					for v in f.readlines():
						lines.append(v.replace(" = ", "="))
				with file(path, "w") as f:
					for v in lines:
						f.writelines(v)			
				return True
		self.log.error("can not find '%s'" %filename)
		return False

	def _parseClientServerList(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('List')
		parser.set('List', 'RegionCount', 1)
		parser.set('List', 'Region_%d' %0, 'test_server%d' %1)
		parser.add_section('Region_%d' %0)
		parser.set('Region_%d' %0, 'Count', 1)
		serverip = self.configParser.get('client', 'serverip')
		parser.set('Region_%d' %0, '%d_Title' %0, serverip)
		parser.set('Region_%d' %0, '%d_Address' %0, serverip)
		with file(path, 'w') as f:
   			parser.write(f)

	def _parseClientConfig(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section("Server")
		parser.set("Server", "GameServPort", 5622)
		parser.set("Server", "ErrorReportAddress", "http://211.152.52.45/faq/xsj/jx2/external/accept.php")
		parser.add_section("Client")
		parser.set("Client", "FullScreen", 0)
		parser.set("Client", "PaintFps", 100)
		parser.set("Client", "PrerenderGround", 1)
		parser.set("Client", "word_wrap", 1)
		parser.set("Client", "text_justification", 0)
		parser.set("Client", "install_fonts", 0)
		parser.set("Client", "clear_text_background", 0)
		parser.set("Client", "single_byte_char_set", 0)
		parser.set("Client", "english_message", 1)
		parser.set("Client", "enable_32bits_color", 1)
		parser.add_section("dumper")
		parser.set("dumper", "GameName", "Jx2Vn")
		parser.set("dumper", "Version", "1.08")
		parser.add_section("TIMEAMBIENT")
		parser.set("TIMEAMBIENT", "MIDNIGHT", "0,120,150,180")
		parser.set("TIMEAMBIENT", "DAWN", "0,150,160,190")
		parser.set("TIMEAMBIENT", "MORNING", "0,225,225,225")
		parser.set("TIMEAMBIENT", "FORENOON", "0,255,255,255")
		parser.set("TIMEAMBIENT", "NOON", "0,255,255,255")
		parser.set("TIMEAMBIENT", "DUSK", "0,215,215,215")
		parser.set("TIMEAMBIENT", "EVENING", "0,120,120,120")
		with file(path, 'w') as f:
   			parser.write(f)

	def configClient(self):
		self.log.info("================================================")
		self.log.info("Prepare to config client!")
		if self._isLinux() and not self._checkYesOrNO("do you config client on linux OS?(y/N):"):
			self.log.info("config client on linux OS cancel by user!")
			return False
		dstPath = self.configParser.get("client", "home").strip()
		if os.path.isdir(dstPath):
			self.log.info("remove dir '%s' ..." %dstPath)
			shutil.rmtree(dstPath, False, self._handlerError)		
		try:		
			self.log.info("mkdir '%s' ..." %dstPath)
			os.makedirs(dstPath)
		except Exception, e:
			self.log.error(str(e))
			return False
		resource = self.configParser.get("client", "resource").strip()
		if not os.path.isdir(resource):
			self.log.error("can not find '%s', please check '%s' file" %(resource, self.config))
			return False
		catalog = self.configParser.get("client", "catalog").split(',')
		filedict = {}
		filecount = 0
		for clv in catalog:
			clvpath = os.path.join(resource, clv)
			if not os.path.exists(clvpath):
				self.log.error("can not find '%s', please check '%s' file" %(clvpath, self.config))
				return False
			self.log.info("copy floders '%s' to '%s' ..." %(clvpath, dstPath))
			self._getTreeDict(clvpath, filedict)
			self.log.info("here are %d file(s) need to move" %(len(filedict) - filecount))
			filecount = len(filedict)
			self._copyFolder(clvpath, dstPath)
		if self._checkYesOrNO("do you need a chinese client?(y/N):"):
			specialcatalog = self.configParser.get("client", "special_catalog").strip()
			specialpath = os.path.join(resource, specialcatalog)
			self.log.info("copy floders '%s' to '%s' ..." %(specialpath, dstPath))
			self._copyFolder(specialpath, dstPath)
		self._extractLibrary(dstPath)
		self._extractFiles(dstPath, RC_CLIENT_LIST)
		self._parseIniFile('server_list.ini', self._parseClientServerList, filedict, resource, catalog, dstPath)
		self._parseIniFile('config.ini', self._parseClientConfig, filedict, resource, catalog, dstPath)
		self.log.info("==> config client finished!")

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
	parser = OptionParser(usage="\n  %%prog <Options> [config] [log]\n  notice: please configurate [%s] at first" %RC_CONFIG_FILE)
	parser.add_option(
		"-p", "--packlibrary", action="store_true", dest="p", help="jv2 program and runtime librarys packaged")
	parser.add_option(
		"-c", "--client", action="store_true", dest="c", help="jv2 client automatic configuration")
	parser.add_option(
		"-s", "--server", action="store_true", dest="s", help="jv2 server automatic configuration")
	opts, args = parser.parse_args()
	if opts.p != True and opts.c != True and opts.s != True:
		parser.print_help()
		return False

	config = None
	if len(args) == 0:
		config = AutoConfig(RC_CONFIG_FILE, RC_LOG_FILE)
	elif len(args) == 1:
		config = AutoConfig(args[0], RC_LOG_FILE)
	elif len(args) == 2:
		config = AutoConfig(args[0], args[1])
	else:
		parser.print_help()
		return False

	if opts.p:
		config.packLibrary(RC_COMMON_PACK)
	if opts.c:
		config.configClient()
	if opts.s:
		config.configServer()

	raw_input("\nplease input any key exit...")

if __name__ == '__main__':
	main()