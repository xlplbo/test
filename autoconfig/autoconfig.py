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
import MySQLdb
import cx_Oracle
import random
import string
import socket
import uuid
import hashlib

RC_LOG_FILE = "autoconfig.log"
RC_CONFIG_FILE = "config.ini"
RC_WINDOW_PACK = "windll.zip"
RC_COMMON_PACK = "data.zip" 
RC_EXT_OR_ELF = ('.dll', '.exe', ".so", ".a", 'kg_goddess', 'kg_bishop', 'so2relay', 'so2gamesvr')
RC_CLIENT_LIST = ('curl.exe', 'engine.dll', 'lualibdll.dll', 'represent3.dll', 'sound.dll', 'dumper.dll',
	'dumpreport.exe', 'verify_up2date.exe', 'so2game.exe', 'rainbow.dll')
RC_GODDESS_LIST = ('engine.dll', 'heaven.dll', 'kg_angel.dll', 'kg_goddess.exe', 'libmysql.dll', 
	'lualibdll.dll', 'verify_up2date.exe')
RC_BISHOP_LIST = ('engine.dll', 'heaven.dll', 'kg_angel.dll', 'kg_bishop.exe', 'libmysql.dll', 
	'lualibdll.dll', 'verify_up2date.exe')
RC_RELAY_LIST = ('engine.dll', 'kg_angel.dll', 'libmysql.dll', 'logdatabase.dll', 'lualibdll.dll', 
	'so2relay.exe', 'verify_up2date.exe')
RC_GAMESVR_LIST = ('engine.dll', 'heaven.dll', 'libmysql.dll', 'logdatabase.dll', 'lualibdll.dll', 'rainbow.dll',
	'so2gamesvr.exe', 'verify_up2date.exe')
RC_ROUTER_LIST = ('engine.dll', 'lualibdll.dll', 'router.exe', 'verify_up2date.exe')
RC_MAX_SIZE = 8192 #MB

class AutoConfig(object):
	"""docstring for AutoConfig"""
	def __init__(self, config, log):
		super(AutoConfig, self).__init__()
		self.paysys_regname = ''.join(random.sample(string.ascii_letters, 8))
		self.paysys_regpasswd = "a"
		self.localIp = self._getLocalIp()
		self.localMac = self._getLocalMac()
		self.config = config
		self.configParser = ConfigParser.ConfigParser()
		self.configParser.readfp(codecs.open(config, "r", self._getFileCoding(config)))  
		self.log = logging.getLogger(log)
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

	def _getLocalIp(self):
		if self._isWondows():
			return socket.gethostbyname(socket.gethostname())
		if self._isLinux():
			import fcntl
			import struct
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			for x in ['eth0', 'wlan0', 'lo']:
				try:
					localip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', x[:15]))[20:24])
					self.log.info("assign requested address %s --> %s" %(x, localip))
					return localip
				except Exception, e:
					self.log.error("%s --> %s" %(str(e), x))
			exit()

	def _getLocalMac(self):
		node = uuid.getnode()
		mac = uuid.UUID(int = node).hex[-12:].upper()
		return "%s-%s-%s-%s-%s-%s" %(mac[:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])

	def _getFileCoding(self, filename):
		charset = None
		with file(filename, "r") as f:
			charset = chardet.detect(f.read())
		return charset['encoding']

	def _checkYesOrNO(self, title):
		while True:
			ret = raw_input(title)
			if ret.lower() == 'n' or ret.lower() == 'no':
				return False
			elif ret.lower() == 'y' or ret.lower() == 'yes':
				return True
			else:
				title = "please input again(y/N):"

	def checkIpCorrectness(self):
		self.log.info("local machine IP: '%s'" %self.localIp)
		if self._checkYesOrNO("if the IP is false, please correct it! do you want to modify?(y/N)"):
			while True:
				msg = "please input IP:"
				ip = raw_input(msg)
				ipformat = ip.split('.')
				if len(ipformat) != 4 or len(filter(lambda x: x >= 0 and x <= 255, map(int, filter(lambda x: x.isdigit(), ipformat)))) != 4:
					self.log.error("does not conform to the rules, input again!")
					continue
				if self._checkYesOrNO("your IP is '%s', right?(y/N):" %ip):
					self.localIp = ip
					break

	def _macFilter(self, s):
		if len(s) != 2:
			return False
		if s[0] not in string.ascii_uppercase and s[0] not in string.digits:
			return False
		if s[1] not in string.ascii_uppercase and s[1] not in string.digits:
			return False
		return True

	def checkMacCorrectness(self):
		self.log.info("local machine MAC: '%s'" %self.localMac)
		if self._checkYesOrNO("if the MAC is false, please correct it! do you want to modify?(y/N)"):
			while True:
				msg = "please input MAC(use upper case):"
				mac = raw_input(msg)
				macformat = mac.split('-')
				if len(macformat) != 6 or len(filter(self._macFilter, macformat)) != 6:
					self.log.error("does not conform to the rules, input again!")
					continue
				if self._checkYesOrNO("your MAC is '%s', right?(y/N):" %mac):
					self.localMac = mac
					break

	def _handlerError(self, func, path, excinfo):
		os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
		func(path)
		self.log.info("Exception handling: %s %s" %(getattr(func, '__name__'), path))

	def _removeFileOrDir(self, path, log = True):
		if os.path.exists(path):
			if log:
				self.log.info("remove '%s' ..." %path)
			if os.path.isdir(path):
				shutil.rmtree(path, False, self._handlerError)
			else:
				os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
				os.remove(path)

	def _makeDir(self, path, delete = True, log = True):
		try:
			if delete:
				self._removeFileOrDir(path, log)
			if not os.path.exists(path):
				if log:
					self.log.info("mkdir '%s' ..." %path)
				os.makedirs(path)
		except Exception, e:
			self.log.error(str(e))
			return False
		return True

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

	def _getProgramsAndLibrary(self, path):
		filedict = {}
		for root, dirs, files in os.walk(path):
			for tup in [(f, os.path.join(root, f)) for f in files if self._isProgramsAndLibrary(f)]:
				filedict[tup[0]] = tup[1]
		return filedict

	def packLibrary(self, name):
		self.log.info("================================================")
		self.log.info("prepare to packaged programs and librarys!")
		self.log.warn("please compile your project at first, and then run packaged program!")
		currPath = os.path.abspath(".")
		for v in os.listdir(currPath):
			if os.path.isfile(v) and v == name:
				if self._checkYesOrNO("check file '%s' is exist! do you update this file?(y/N):" %name):
					self._removeFileOrDir(name)
				else:
					self.log.info("packaged finish! thanks all")
					return True
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
			filedict = self._getProgramsAndLibrary(pathlv)
			if len(filedict) <= 0:
				continue
			zipFile = zipfile.ZipFile(name, 'a', zipfile.ZIP_DEFLATED)
			for k, v in filedict.iteritems():
				self.log.info("file '%s' packaged" %k)
				zipFile.write(v, k)
			zipFile.close()
		self.log.info("==> generate '%s' success! " %name)
		self.log.info("==> packaged programs and librarys finished!")

	def _getFileCount(self, path, blacklist):
		count = 0L
		for root, dirs, files in os.walk(path):
			if len([x for x in blacklist if x in root]) > 0:
				continue
			count += files.__len__() - len([x for x in files for y in blacklist if y in x])
		return count

	def _getDirSize(self, dir):
		size = 0L
		for root, dirs, files in os.walk(dir):
			size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
		return size/1024/1024

	def _createShortcut(self, src, dst):
		import pythoncom
		from win32com.shell import shell
		shortcut = pythoncom.CoCreateInstance(
		shell.CLSID_ShellLink, None,
		pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
		shortcut.SetPath(src)
		if os.path.splitext(dst)[-1] != '.lnk':  
			dst += ".lnk" 
		shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(dst,0)
		self.log.info("create shortcut '%s' ..." %dst)

	def _copyFile(self, srcname, dstname):
		try:
			self._removeFileOrDir(dstname)
			if os.path.isfile(srcname):
				shutil.copy2(srcname, dstname)
				shutil.copystat(srcname, dstname)
		except Exception, e:
			self.log.error(str(e))

	def _copyFolder(self, src, dst, blacklist):
		filecount = 0L
		lnkfilecount = 0L
		filetotal = self._getFileCount(src, blacklist)
		step = (filetotal - filetotal%10) / 10
		lnklist = []
		for root, dirs, files in os.walk(src):
			if len([x for x in blacklist if x in root]) > 0:
				continue
			if len([x for x in lnklist if x in root]) > 0:
				continue
			dstroot = root.replace(src, dst)
			self._makeDir(dstroot, False, False)
			for dir in [x for x in dirs if x not in blacklist]:
				srcPath = os.path.join(root, dir)
				dstpath = os.path.join(dstroot, dir)
				if self._isWondows():
					if self._getDirSize(srcPath) < RC_MAX_SIZE:				
						self._makeDir(dstpath, False, False)
					else:
						lnklist.append(srcPath)
						self._createShortcut(srcPath, dstpath)
						count = self._getFileCount(srcPath, blacklist)
						lnkfilecount = count
						filecount += count
						if step > 0:
							index = filecount // step
							if index <= 10 and index * step == filecount:
								self.log.info("progress %d%%" %(index*10))
						elif filecount == filetotal:
							self.log.info("progress %d%%" %100)
				else:
					self._makeDir(dstpath, False, False)
			for file in [x for x in files if x not in blacklist]:
				srcfile = os.path.join(root, file)
				dstfile = os.path.join(dstroot, file)
				self._copyFile(srcfile, dstfile)
				filecount += 1
				if step > 0:
					index = filecount // step
					if index <= 10 and index * step == filecount:
						self.log.info("progress %d%%" %(index*10))
				elif filecount == filetotal:
					self.log.info("progress %d%%" %100)
		self.log.info("actually %d file(s) have been copied" %(filecount-lnkfilecount))

	def copyFolder(self, src, dst, blacklist = []):
		if not os.path.exists(src):
			self.log.error("can not find '%s', please check '%s' file" %(src, self.config))
		if not os.path.exists(dst):
			self.log.error("can not find '%s', please check '%s' file" %(dst, self.config))
		self.log.info("copy floders '%s' to '%s' ..." %(src, dst))
		blacklist.append(".svn")
		self._copyFolder(src, dst, map(lambda s: s.lower(), blacklist))

	def _extractLibrary(self, path):
		self.log.info("copy windows librarys to '%s'" %path)
		zipFile = zipfile.ZipFile(RC_WINDOW_PACK, 'r', zipfile.ZIP_DEFLATED)
		for v in zipFile.namelist():
			try:
				zipFile.extract(v, path)
				self.log.info("extract '%s' ..." %v)
			except Exception, e:
				self.log.error(str(e))			

	def _extractFiles(self, path, list):
		self.log.info("copy programs and librarys to '%s'" %path)
		zipFile = zipfile.ZipFile(RC_COMMON_PACK, 'r', zipfile.ZIP_DEFLATED)
		extFile = []
		for v in zipFile.namelist():
			lfile = v.lower()
			lfiled = lfile.replace('d.', '.')
			try:
				if lfile in list and lfile not in extFile:
					zipFile.extract(v, path)
					extFile.append(lfile)
					self.log.info("extract '%s' ..." %v)
				elif lfiled in list and lfiled not in extFile:
					zipFile.extract(v, path)
					extFile.append(lfiled)
					self.log.info("extract '%s' ..." %v)
			except Exception, e:
				self.log.error(str(e))			
		for v in list:
			if v not in extFile:
				self.log.error("can not find '%s', please check '%s' file" %(v, RC_COMMON_PACK))

	def _parseIniFile(self, root, filename, func, *param, **kw):
		if self._isWondows():
			root = root.replace("/", "\\")
			filename = filename.replace("/", "\\")
		if self._isLinux():
			root = root.replace("\\", "/")
			filename = filename.replace("\\", "/")
		filepath = os.path.join(root, filename)
		if not os.path.isfile(filepath):
			self.log.error("can not find '%s'" %filepath)
		self.log.info("parser INI file '%s'" %filepath)
		if len(param) == 0:
			func(filepath)
		else:
			func(filepath, *param, **kw)
		lines = []
		with file(filepath, "r") as f:
			for v in f.readlines():
				lines.append(v.replace(" = ", "="))
		with file(filepath, "w") as f:
			for v in lines:
				f.writelines(v)			
		return True

	def _parseClientServerList(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('List')
		parser.set('List', 'RegionCount', 1)
		parser.set('List', 'Region_%d' %0, 'test_server%d' %1)
		parser.add_section('Region_%d' %0)
		parser.set('Region_%d' %0, 'Count', 1)
		serverip = self.configParser.get('client', 'serverip')
		if not serverip or serverip == "0":
			serverip = self.localIp
		parser.set('Region_%d' %0, '%d_Title' %0, serverip)
		parser.set('Region_%d' %0, '%d_Address' %0, serverip)
		with file(path, 'w') as f:
   			parser.write(f)

	def _parseClientConfig(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section("Server")
		parser.set("Server", "GameServPort", 5622)
		parser.set("Server", "ErrorReportAddress", "http://reporting.volam2.zing.vn")
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
		if not os.path.exists(RC_COMMON_PACK):
			self.log.error("can not find '%s', abort!!!" %RC_COMMON_PACK)
			self.log.info("please run program with '-p', packaged programs and librarys!")
			return False
		if self._isLinux():
			self.log.info("config client on linux OS, abort!!!")
			return False
		root = self.configParser.get("client", "home").strip()
		if not self._makeDir(root):
			return False
		resource = self.configParser.get("client", "resource").strip()
		if not os.path.isdir(resource):
			self.log.error("can not find '%s', please check '%s' file" %(resource, self.config))
			return False
		catalog = self.configParser.get("client", "catalog").split(',')
		for clv in catalog:
			clvpath = os.path.join(resource, clv)
			self.copyFolder(clvpath, root)
		specialcatalog = self.configParser.get("client", "special_catalog").strip()
		specialpath = os.path.join(resource, specialcatalog)
		if os.path.exists(specialpath):
			self.copyFolder(specialpath, root)
		self._extractLibrary(root)
		self._extractFiles(root, RC_CLIENT_LIST)
		self._parseIniFile(root, "settings/server_list.ini", self._parseClientServerList)
		self._parseIniFile(root, "config.ini", self._parseClientConfig)
		self.log.info("==> config client finished!")

	def _parseGoddessConfig(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Version')
		parser.set('Version', 'Version', 2)
		parser.add_section('KG_Goddess')
		parser.set('KG_Goddess', 'ListenIP', self.localIp)
		parser.set('KG_Goddess', 'ListenPort', 5001)
		parser.set('KG_Goddess', 'LoopSleepTime', 10)
		parser.set('KG_Goddess', 'AutoDisconnectTime', 120000)
		parser.set('KG_Goddess', 'SendRecvTimeout', 60000)
		parser.set('KG_Goddess', 'Group', 1)
		parser.set('KG_Goddess', 'MaxRoleCountInAccount', 9)
		parser.add_section('DatabaseServer')
		parser.set('DatabaseServer', 'Server', self.configParser.get("mysql", "ip"))
		parser.set('DatabaseServer', 'UserName', self.configParser.get("mysql", "username"))
		parser.set('DatabaseServer', 'Database', self.configParser.get("mysql", "database"))
		parser.set('DatabaseServer', 'Password', self.configParser.get("mysql", "password"))
		parser.set('DatabaseServer', 'EnableEncrypt', 0)
		parser.add_section('RoleStatistic')
		parser.set('RoleStatistic', 'ListenIP', self.localIp)
		parser.set('RoleStatistic', 'ListenPort', 6001)
		parser.set('RoleStatistic', 'SendRecvTimeout', 60000)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _parseBishopConfig(self, path):
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Version')
		parser.set('Version', 'Version', "bishop2")
		parser.add_section('Paysys')
		parser.set('Paysys', 'IPAddress', self.configParser.get("paysys", "ip"))
		parser.set('Paysys', 'Port', self.configParser.get("paysys", "port"))
		parser.set('Paysys', 'UserName', self.paysys_regname)
		parser.set('Paysys', 'Password', self.paysys_regpasswd)
		parser.set('Paysys', 'SendRecvTimeout', 60000)
		parser.set('Paysys', 'ReconnectTime', 10000)
		parser.set('Paysys', 'LoopTime', 100)
		parser.set('Paysys', 'PingTime', 10000)
		parser.add_section('Goddess')
		parser.set('Goddess', 'IPAddress', self.localIp)
		parser.set('Goddess', 'LocalIPAddress', self.localIp)
		parser.set('Goddess', 'Port', 5001)
		parser.set('Goddess', 'SendRecvTimeout', 60000)
		parser.set('Goddess', 'ReconnectTime', 10000)
		parser.set('Goddess', 'LoopTime', 100)
		parser.set('Goddess', 'PingTime', 20000)
		parser.add_section('Relay')
		parser.set('Relay', 'LocalIPAddress', self.localIp)
		parser.set('Relay', 'OpenPort', 5632)
		parser.set('Relay', 'SendRecvTimeout', 60000)
		parser.set('Relay', 'LoopTime', 100)
		parser.set('Relay', 'PingTime', 20000)
		parser.set('Relay', 'AccountInRelayTimeout', 60000)
		parser.add_section('GameServer')
		parser.set('GameServer', 'LocalIPAddress', self.localIp)
		parser.set('GameServer', 'OpenPort', 5633)
		parser.set('GameServer', 'SendRecvTimeout', 180000)
		parser.set('GameServer', 'AccountInManagerTimeout', 300000)
		parser.set('GameServer', 'LoopTime', 100)
		parser.set('GameServer', 'PingTime', 60000)
		parser.add_section('Player')
		parser.set('Player', 'LocalIPAddress', self.localIp)
		parser.set('Player', 'OpenPort', 5622)
		parser.set('Player', 'MaxPlayers', 16)
		parser.set('Player', 'MaxPlayerInLoginSection', 10)
		parser.set('Player', 'SendRecvTimeout', 180000)
		parser.set('Player', 'PlayerOperateTimeout', 60000)
		parser.set('Player', 'IBSupport', 1)
		parser.add_section('LiveTimeLogger')
		parser.set('LiveTimeLogger', 'LiveTimeLoggerLoopTime', 5000)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _parseRelayConfig(self, path):
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Gmc')
		parser.set('Gmc', 'Address', self.configParser.get("paysys", "ip"))
		parser.set('Gmc', 'LocalAddr', self.localIp)
		parser.set('Gmc', 'Port', 9991)
		parser.set('Gmc', 'Enable', 0)
		parser.set('Gmc', 'EncryptionType', 0)
		parser.set('Gmc', 'ReConnInterval', 20000)
		parser.set('Gmc', 'PingInterval', 90000)		
		parser.add_section('Bishop')
		parser.set('Bishop', 'Address', self.localIp)
		parser.set('Bishop', 'LocalAddr', self.localIp)
		parser.set('Bishop', 'Port', 5632)
		parser.set('Bishop', 'Enable', 1)
		parser.set('Bishop', 'EncryptionType', 0)
		parser.set('Bishop', 'ReConnInterval', 20000)
		parser.set('Bishop', 'PingInterval', 90000)
		parser.add_section('Goddess')
		parser.set('Goddess', 'Address', self.localIp)
		parser.set('Goddess', 'LocalAddr', self.localIp)
		parser.set('Goddess', 'Port', 5001)
		parser.set('Goddess', 'Enable', 1)
		parser.set('Goddess', 'EncryptionType', 0)
		parser.set('Goddess', 'CheckConnInterval', 30000)
		parser.add_section('Relay')
		parser.set('Relay', 'PlayerCnt', 10)
		parser.set('Relay', 'precision', 1)
		parser.set('Relay', 'FreeBuffer', 15)
		parser.set('Relay', 'BufferSize', 1048576)
		parser.set('Relay', 'backup', 0)
		parser.add_section('Host')
		parser.set('Host', 'bLogSocket', 1)
		parser.set('Host', 'LocalAddr', self.localIp)
		parser.set('Host', 'ListenPort', 5003)
		parser.set('Host', 'SendRecvTimeout', 60000)
		parser.set('Host', 'LoopTime', 50)
		parser.set('Host', 'PingTime', 60000)
		parser.set('Host', 'PlayerCnt', 10)
		parser.set('Host', 'Precision', 1)
		parser.set('Host', 'FreeBuffer', 15)
		parser.set('Host', 'BufferSize', 1048576)
		parser.add_section('Chat')
		parser.set('Chat', 'LocalAddr', self.localIp)
		parser.set('Chat', 'ListenPort', 5004)
		parser.set('Chat', 'SendRecvTimeout', 60000)
		parser.set('Chat', 'LoopTime', 50)
		parser.set('Chat', 'PlayerCnt', 10)
		parser.set('Chat', 'Precision', 1)
		parser.set('Chat', 'FreeBuffer', 15)
		parser.set('Chat', 'BufferSize', 409600)
		parser.add_section('Tong')
		parser.set('Tong', 'LocalAddr', self.localIp)
		parser.set('Tong', 'ListenPort', 5005)
		parser.set('Tong', 'SendRecvTimeout', 60000)
		parser.set('Tong', 'LoopTime', 50)
		parser.set('Tong', 'PlayerCnt', 10)
		parser.set('Tong', 'Precision', 1)
		parser.set('Tong', 'FreeBuffer', 15)
		parser.set('Tong', 'BufferSize', 1048576)
		parser.set('Tong', 'flushinterval', 30)
		parser.add_section('Log')
		parser.set('Log', 'FacSayLog', 1)
		parser.add_section('DataBase')
		parser.set('DataBase', 'DBHost', self.configParser.get("mysql", "ip"))
		parser.set('DataBase', 'DBName', self.configParser.get("mysql", "database"))
		parser.set('DataBase', 'LogDBName', "%s_log" %self.configParser.get("mysql", "database"))
		parser.set('DataBase', 'DBUser', self.configParser.get("mysql", "username"))
		parser.set('DataBase', 'DBPwd', self.configParser.get("mysql", "password"))
		parser.set('DataBase', 'DBGroup',1 )
		parser.set('DataBase', 'DBPort', 3306)
		parser.set('DataBase', 'EnableEncrypt', 0)
		parser.add_section('GlobalDatabase')
		parser.set('GlobalDatabase', 'Server', self.configParser.get("mysql", "ip"))
		parser.set('GlobalDatabase', 'Database', "jx2vn_global_db")
		parser.set('GlobalDatabase', 'User', self.configParser.get("mysql", "username"))
		parser.set('GlobalDatabase', 'Password', self.configParser.get("mysql", "password"))
		parser.set('GlobalDatabase', 'Port', 3306)
		parser.set('GlobalDatabase', 'EnableEncrypt', 0)
		parser.add_section('MyGlbDB')
		parser.set('MyGlbDB', 'Server', self.configParser.get("mysql", "ip"))
		parser.set('MyGlbDB', 'Database', "jx2vn_global_db")
		parser.set('MyGlbDB', 'User', self.configParser.get("mysql", "username"))
		parser.set('MyGlbDB', 'Password', self.configParser.get("mysql", "password"))
		parser.set('MyGlbDB', 'Port', 3306)
		parser.set('MyGlbDB', 'EnableEncrypt', 0)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _parseGRelayConfig(self, path, ip, **kw):
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Gmc')
		parser.set('Gmc', 'Address', self.configParser.get("paysys", "ip"))
		parser.set('Gmc', 'LocalAddr', ip)
		parser.set('Gmc', 'Port', 9991)
		parser.set('Gmc', 'Enable', 0)
		parser.set('Gmc', 'EncryptionType', 0)
		parser.set('Gmc', 'ReConnInterval', 20000)
		parser.set('Gmc', 'PingInterval', 90000)		
		parser.add_section('Bishop')
		parser.set('Bishop', 'Address', ip)
		parser.set('Bishop', 'LocalAddr', ip)
		parser.set('Bishop', 'Port', 5632)
		parser.set('Bishop', 'Enable', 0)
		parser.set('Bishop', 'EncryptionType', 0)
		parser.set('Bishop', 'ReConnInterval', 20000)
		parser.set('Bishop', 'PingInterval', 90000)
		parser.add_section('Goddess')
		parser.set('Goddess', 'Address', ip)
		parser.set('Goddess', 'LocalAddr', ip)
		parser.set('Goddess', 'Port', 5001)
		parser.set('Goddess', 'Enable', 0)
		parser.set('Goddess', 'EncryptionType', 0)
		parser.set('Goddess', 'CheckConnInterval', 30000)
		parser.add_section('Relay')
		parser.set('Relay', 'PlayerCnt', 10)
		parser.set('Relay', 'precision', 1)
		parser.set('Relay', 'FreeBuffer', 15)
		parser.set('Relay', 'BufferSize', 1048576)
		parser.set('Relay', 'backup', 0)
		parser.add_section('Host')
		parser.set('Host', 'bLogSocket', 1)
		parser.set('Host', 'LocalAddr', ip)
		parser.set('Host', 'ListenPort', 5003)
		parser.set('Host', 'SendRecvTimeout', 60000)
		parser.set('Host', 'LoopTime', 50)
		parser.set('Host', 'PingTime', 60000)
		parser.set('Host', 'PlayerCnt', 10)
		parser.set('Host', 'Precision', 1)
		parser.set('Host', 'FreeBuffer', 15)
		parser.set('Host', 'BufferSize', 1048576)
		parser.add_section('Chat')
		parser.set('Chat', 'LocalAddr', ip)
		parser.set('Chat', 'ListenPort', 5004)
		parser.set('Chat', 'SendRecvTimeout', 60000)
		parser.set('Chat', 'LoopTime', 50)
		parser.set('Chat', 'PlayerCnt', 10)
		parser.set('Chat', 'Precision', 1)
		parser.set('Chat', 'FreeBuffer', 15)
		parser.set('Chat', 'BufferSize', 409600)
		parser.add_section('Tong')
		parser.set('Tong', 'LocalAddr', ip)
		parser.set('Tong', 'ListenPort', 5005)
		parser.set('Tong', 'SendRecvTimeout', 60000)
		parser.set('Tong', 'LoopTime', 50)
		parser.set('Tong', 'PlayerCnt', 10)
		parser.set('Tong', 'Precision', 1)
		parser.set('Tong', 'FreeBuffer', 15)
		parser.set('Tong', 'BufferSize', 1048576)
		parser.set('Tong', 'flushinterval', 30)
		parser.add_section('Log')
		parser.set('Log', 'FacSayLog', 1)
		parser.add_section('DataBase')
		parser.set('DataBase', 'DBHost', kw["host"])
		parser.set('DataBase', 'DBName', kw["db"])
		parser.set('DataBase', 'LogDBName', "%s_log" %kw["db"])
		parser.set('DataBase', 'DBUser', kw["user"])
		parser.set('DataBase', 'DBPwd', kw["passwd"])
		parser.set('DataBase', 'DBGroup',1 )
		parser.set('DataBase', 'DBPort', 3306)
		parser.set('DataBase', 'EnableEncrypt', 0)
		parser.add_section('GlobalDatabase')
		parser.set('GlobalDatabase', 'Server', kw["host"])
		parser.set('GlobalDatabase', 'Database', "jx2vn_global_db")
		parser.set('GlobalDatabase', 'User', kw["user"])
		parser.set('GlobalDatabase', 'Password', kw["passwd"])
		parser.set('GlobalDatabase', 'Port', 3306)
		parser.set('GlobalDatabase', 'EnableEncrypt', 0)
		parser.add_section('MyGlbDB')
		parser.set('MyGlbDB', 'Server', kw["host"])
		parser.set('MyGlbDB', 'Database', "jx2vn_global_db")
		parser.set('MyGlbDB', 'User', kw["user"])
		parser.set('MyGlbDB', 'Password', kw["passwd"])
		parser.set('MyGlbDB', 'Port', 3306)
		parser.set('MyGlbDB', 'EnableEncrypt', 0)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _parseRouterConfig(self, path, *param):
   		if len(param) != 2:
   			self.log.error("can not get mainip and subip %s! abort." %str(param))
   			exit()
   		mainip = param[0]
   		subip = param[-1]
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('BaseInfo')
		parser.set('BaseInfo', 'IOTimeout', 0)
		parser.set('BaseInfo', 'ReconnectCycle', 0)
		parser.set('BaseInfo', 'PingCycle', 0)
		parser.set('BaseInfo', 'WorkLoopCycle', 0)
		parser.set('BaseInfo', 'SaveRoleData', 0)
		parser.set('BaseInfo', 'LocalIP', mainip)
		parser.set('BaseInfo', 'ExternalIP', mainip)
		parser.set('BaseInfo', 'Port', 8888)
		parser.set('BaseInfo', 'MaxPlayer', 20)
		parser.add_section('LocalAddrList')
		parser.set('LocalAddrList', 'LocAddrCount', 2)
		parser.set('LocalAddrList', 'LocAddr_0', mainip)
		parser.set('LocalAddrList', 'LocAddr_1', subip)
		parser.add_section('LocalGSSrvInfo')
		parser.set('LocalGSSrvInfo', 'GameServerCount', 1)
		parser.set('LocalGSSrvInfo', 'LocalAddr', mainip)
		parser.set('LocalGSSrvInfo', 'BishopSrvOpenPort', 8871)
		parser.set('LocalGSSrvInfo', 'GoddessSrvOpenPort', 8872)
		parser.set('LocalGSSrvInfo', 'RelayHostSrvOpenPort', 8873)
		parser.set('LocalGSSrvInfo', 'RelayChatSrvOpenPort', 8874)
		parser.set('LocalGSSrvInfo', 'RelayTongSrvOpenPort', 8875)
		parser.add_section('LocalRelayInfo')
		parser.set('LocalRelayInfo', 'LocRelayAddr', mainip)
		parser.set('LocalRelayInfo', 'LocRelayHostPort', 5003)
		parser.set('LocalRelayInfo', 'LocRelayChatPort', 5004)
		parser.set('LocalRelayInfo', 'LocRelayTongPort', 5005)
		parser.add_section('OriginGroupInfo')
		parser.set('OriginGroupInfo', 'OriginGroupCount', 1)
		parser.add_section('PATH')
		parser.set('PATH', 'ScriptFolder', "script/")
		parser.set('PATH', 'ScriptFileName', "routerscript.lua")
		parser.add_section('OriginGroupInfo_0')
		originIP = None
		while True:
			ip = raw_input("please input Origin Gateway Ip Address:")
			ipformat = ip.split('.')
			if len(ipformat) != 4 or len(filter(lambda x: x >= 0 and x <= 255, map(int, filter(lambda x: x.isdigit(), ipformat)))) != 4:
				self.log.error("does not conform to the rules, input again!")
				continue
			if self._checkYesOrNO("your IP is '%s', right?(y/N):" %ip):
				originIP = ip
				break
		parser.set('OriginGroupInfo_0', 'GroupName', originIP.split(".")[-1])
		parser.set('OriginGroupInfo_0', 'BishopAddr', originIP)
		parser.set('OriginGroupInfo_0', 'BishopPort', 5633)
		parser.set('OriginGroupInfo_0', 'GoddessAddr', originIP)
		parser.set('OriginGroupInfo_0', 'GoddessPort', 5001)
		parser.set('OriginGroupInfo_0', 'RelayAddr', originIP)		
		parser.set('OriginGroupInfo_0', 'RelayHostPort', 5003)
		parser.set('OriginGroupInfo_0', 'RelayChatPort', 5004)
		parser.set('OriginGroupInfo_0', 'RelayTongPort', 5005)
		with file(path, 'w') as f:
   			parser.write(f)

	def _configGoddess(self, dstPath):
		self._extractFiles(dstPath, RC_GODDESS_LIST)
		self._parseIniFile(dstPath, "KG_Goddess.ini", self._parseGoddessConfig)

	def _configBishop(self, dstPath):
		self._extractFiles(dstPath, RC_BISHOP_LIST)
		self._parseIniFile(dstPath, "bishop.ini", self._parseBishopConfig)

	def _configRelay(self, dstPath):
		self._extractFiles(dstPath, RC_RELAY_LIST)
		self._parseIniFile(dstPath, "relay.ini", self._parseRelayConfig)

	def _configGRelay(self, dstPath, *param, **kw):
		self._extractFiles(dstPath, RC_RELAY_LIST)
		self._parseIniFile(dstPath, "relay.ini", self._parseGRelayConfig, *param, **kw)

	def _configRouter(self, dstPath, *param):
		self._extractFiles(dstPath, RC_ROUTER_LIST)
		self._parseIniFile(dstPath, "Router.ini", self._parseRouterConfig, *param)

	def _configGateway(self, name, root, resource, catalog, func, *param, **kw):
		self.log.info("================================================")
		self.log.info("==> begin to config %s ..." %name)
		dstPath = os.path.join(root, name)
		if not self._makeDir(dstPath):
			return False
		src = [os.path.join(resource, v) for v in catalog][0]
		srcPath = os.path.join(src, name)
		if not os.path.isdir(srcPath):
			self.log.error("can not find '%s' path" %srcPath)
			return False
		self.copyFolder(srcPath, dstPath)
		special_catalog = self.configParser.get("server", "special_catalog")
		specialpath = os.path.join(resource, special_catalog, name)
		if not os.path.isdir(specialpath):
			self.log.error("can not find '%s' path" %specialpath)
			return False
		self.copyFolder(specialpath, dstPath)
		self._extractLibrary(dstPath)
		if len(param) == 0:
			func(dstPath)
		else:
			srcPath = os.path.join(src, "G%s" %name)
			if not os.path.isdir(srcPath):
				self.log.error("can not find '%s' path" %srcPath)
			else:
				self.copyFolder(srcPath, dstPath)
			special_catalog = self.configParser.get("server", "special_catalog")
			specialpath = os.path.join(resource, special_catalog, "G%s" %name)
			if not os.path.isdir(specialpath):
				self.log.error("can not find '%s' path" %specialpath)
			else:
				self.copyFolder(specialpath, dstPath)
			func(dstPath, *param, **kw)
		self.log.info("==> config %s finished!" %name)

	def _parseGamesvr(self, path):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Server')
		parser.set('Server', 'ServerCount', 5)
		parser.set('Server', 'ServerIndex', "1,2,3")
		parser.set('Server', 'IS_KINGSOFT_INNER_VERSION_acc_jh34ji84r347e8T56', 0)
		parser.set('Server', 'IS_EXP_SVR', 0)
		parser.set('Server', 'IS_INTERNAL_TEST_SVR', 1)
		parser.add_section('Gateway')
		parser.set('Gateway', 'Ip', self.localIp)
		parser.set('Gateway', 'Port', 5633)
		parser.add_section('Database')
		parser.set('Database', 'Ip', self.localIp)
		parser.set('Database', 'Port', 5001)
		parser.add_section('Transfer')
		parser.set('Transfer', 'Ip', self.localIp)
		parser.set('Transfer', 'Port', 5003)
		parser.add_section('Chat')
		parser.set('Chat', 'Ip', self.localIp)
		parser.set('Chat', 'Port', 5004)
		parser.add_section('Tong')
		parser.set('Tong', 'Ip', self.localIp)
		parser.set('Tong', 'Port', 5005)
		parser.add_section('GameServer')
		parser.set('GameServer', 'Port', 6667)
		parser.set('GameServer', 'GM', 1)
		parser.add_section('Net')
		parser.set('Net', 'LocalIP', self.localIp)
		parser.set('Net', 'ExternalIP', self.localIp)
		parser.add_section('Overload')
		parser.set('Overload', 'MaxPlayer', 2000)
		parser.set('Overload', 'Precision', 50)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _configGs(self, path):
   		self._parseIniFile(path, "servercfg.ini", self._parseGamesvr)

   	def _parseGGamesvr(self, path, ip):
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Server')
		parser.set('Server', 'ServerCount', 5)
		parser.set('Server', 'ServerIndex', 6)
		parser.set('Server', 'RealmType', 1)
		parser.set('Server', 'IsMatchRealm', "true")
		parser.set('Server', 'bLogRelayPacket', 1)
		parser.set('Server', 'IS_KINGSOFT_INNER_VERSION_acc_jh34ji84r347e8T56', 0)
		parser.set('Server', 'IS_EXP_SVR', 0)
		parser.set('Server', 'IS_INTERNAL_TEST_SVR', 1)
		parser.add_section('Gateway')
		parser.set('Gateway', 'Ip', ip)
		parser.set('Gateway', 'Port', 8871)
		parser.add_section('Database')
		parser.set('Database', 'Ip', ip)
		parser.set('Database', 'Port', 8872)
		parser.add_section('Transfer')
		parser.set('Transfer', 'Ip', ip)
		parser.set('Transfer', 'Port', 8873)
		parser.add_section('Chat')
		parser.set('Chat', 'Ip', ip)
		parser.set('Chat', 'Port', 8874)
		parser.add_section('Tong')
		parser.set('Tong', 'Ip', ip)
		parser.set('Tong', 'Port', 8875)
		parser.add_section('GameServer')
		parser.set('GameServer', 'Port', 8889)
		parser.set('GameServer', 'GM', 1)
		parser.add_section('Net')
		parser.set('Net', 'LocalIP', ip)
		parser.set('Net', 'ExternalIP', ip)
		parser.add_section('Overload')
		parser.set('Overload', 'MaxPlayer', 2000)
		parser.set('Overload', 'Precision', 50)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _configGGs(self, path, *param):
   		self._parseIniFile(path, "servercfg.ini", self._parseGGamesvr, *param)

	def _configGameSvr(self, root, resource, catalog, func, *param):
		self.log.info("================================================")
		name = "GameSvr"
		extname = "GGameSvr"
		self.log.info("==> begin to config %s ..." %name)
		dstPath = os.path.join(root, name)
		if not self._makeDir(dstPath):
			return False
		srcPath = os.path.join(resource, catalog[0], name)
		if not os.path.isdir(srcPath):
			self.log.error("can not find '%s' path" %srcPath)
			return False
		self.copyFolder(srcPath, dstPath)
		srcData = os.path.join(resource, catalog[1], "data")
		if not os.path.isdir(srcData):
			self.log.error("can not find '%s' path" %srcData)
			return False
		dataPath = os.path.join(dstPath, "data")
		if not self._makeDir(dataPath):
			return False
		blacklist = ['spr.pak.txt', 'spr.pak', 'resource.pak.txt', 'resource.pak', 'music.pak.txt', 
			'maps_c.pak.txt', 'maps_c.pak', 'font_vn.pak', 'font_cn.pak', 'font.pak.txt', 'music.pak']
		self.copyFolder(srcData, dataPath, blacklist)
		settingsPath = os.path.join(resource, catalog[2])
		if not os.path.isdir(settingsPath):
			self.log.error("can not find '%s' path" %settingsPath)
			return False
		self.copyFolder(settingsPath, dstPath)
		special_catalog = self.configParser.get("server", "special_catalog")
		specialpath = os.path.join(resource, special_catalog, name)
		if not os.path.isdir(specialpath):
			self.log.error("can not find '%s' path" %specialpath)
			return False
		self.copyFolder(specialpath, dstPath)
		self._extractLibrary(dstPath)
		self._extractFiles(dstPath, RC_GAMESVR_LIST)
		if len(param) == 0:
			func(dstPath)
		else:
			srcPath = os.path.join(resource, catalog[0], extname)
			if not os.path.isdir(srcPath):
				self.log.error("can not find '%s' path" %srcPath)
			else:
				self.copyFolder(srcPath, dstPath)
			specialpath = os.path.join(resource, special_catalog, extname)
			if not os.path.isdir(specialpath):
				self.log.error("can not find '%s' path" %specialpath)
			else:
				self.copyFolder(specialpath, dstPath)
			func(dstPath, *param)
		self._removeFileOrDir(os.path.join(dstPath, "dynamic_pwd.ini"))
		self.log.info("==> config %s finished!" %name)

	def configServer(self):
		self.log.info("================================================")
		self.log.info("Prepare to config server!")
		if not os.path.exists(RC_COMMON_PACK):
			self.log.error("can not find '%s', abort!!!" %RC_COMMON_PACK)
			self.log.info("please run program with '-p', packaged programs and librarys!")
			return False
		if not self.configMysql() and not self._checkYesOrNO("mysql operation failed, continue?(y/N):"):
			self.log.info("user cancelled!!!")
			return True
		if not self.registerPaysys(self.paysys_regname, self.paysys_regpasswd) and \
			not self._checkYesOrNO("register paysys operation failed, continue?(y/N):"):
			self.log.info("user cancelled!!!")
			return True
		root = self.configParser.get("server", "home").strip()
		if not self._makeDir(root):
			return False
		resource = self.configParser.get("server", "resource").strip()
		if not os.path.isdir(resource):
			self.log.error("can not find '%s', please check '%s' file" %(resource, self.config))
			return False
		catalog = self.configParser.get("server", "catalog").split(',')
		self._configGateway("Goddess", root, resource, catalog, self._configGoddess)
		self._configGateway("Bishop", root, resource, catalog, self._configBishop)
		self._configGateway("Relay", root, resource, catalog, self._configRelay)
		self._configGameSvr(root, resource, catalog, self._configGs)
		self.log.info("==> config server finished!")

	def configRouter(self):
		self.log.info("================================================")
		self.log.info("Prepare to config GGS!")
		if not os.path.exists(RC_COMMON_PACK):
			self.log.error("can not find '%s', abort!!!" %RC_COMMON_PACK)
			self.log.info("please run program with '-p', packaged programs and librarys!")
			return False
		mysql = dict()
		self.log.info("please input router's mysql information:")
		mysql["host"] = raw_input("mysql IP address:")
		mysql["user"] = raw_input("mysql user name:")
		mysql["passwd"] = raw_input("mysql user passwd:")
		mysql["port"] = int(raw_input("mysql port(e.g:3306):"))
		mysql["db"] = raw_input("mysql database name:")
		if not self._configMysql(**mysql) and not self._checkYesOrNO("mysql operation failed, continue?(y/N):"):
			self.log.info("user cancelled!!!")
			return True
		root = self.configParser.get("router", "home").strip()
		if not self._makeDir(root):
			return False
		resource = self.configParser.get("router", "resource").strip()
		if not os.path.isdir(resource):
			self.log.error("can not find '%s', please check '%s' file" %(resource, self.config))
			return False
		catalog = self.configParser.get("server", "catalog").split(',')
		self.log.info("router need two IPs:")
		mainip = raw_input("main IP address:")
		subip = raw_input("sub IP address:")
		self._configGameSvr(root, resource, catalog, self._configGGs, mainip)
		self._configGateway("Relay", root, resource, catalog, self._configGRelay, mainip, **mysql)
		self._configGateway("Router", root, resource, catalog, self._configRouter, mainip, subip)
		self.log.info("==> config GGS finished!")

	def _configMysql(self, **kw):
		self.log.info("==> connect and operate mysql ...")
		try:
			conn = MySQLdb.connect(host=kw["host"], user=kw["user"], passwd=kw["passwd"], port=kw["port"])
			cur = conn.cursor()
			cur.execute('select @@version')
			format = map(lambda x: x[0], cur.fetchall())
			if len(format) > 0:
				self.log.info("mysql version: '%s'" %format[0])
				vret = format[0].split('.')
				mainversion = int(vret[0])
				subversion = int(vret[1])
				if (mainversion == 5 and subversion > 1) or mainversion < 5:
					self.log.error("mysql version is ERROR!!!, Version 5.1.69 is best" %data)
					cur.close()
					conn.close()
					return False
			cur.execute('show databases')
			format = map(lambda x: x[0], cur.fetchall())
			db = kw["db"]
			if db not in format:
				cur.execute('create database if not exists %s' %db)
				self.log.info("create database '%s' ..." %db)
			self.log.info("find database '%s' OK!" %db)
			if "%s_log" %db not in format:
				cur.execute('create database if not exists %s' %("%s_log" %db))
				self.log.info("create database '%s' ..." %("%s_log" %db))
			self.log.info("find database '%s' OK!" %("%s_log" %db))
			globaldatabase = "jx2vn_global_db"
			if globaldatabase not in format:
				cur.execute('create database if not exists %s' %globaldatabase)
				self.log.info("create database '%s' ..." %globaldatabase)
			self.log.info("find database '%s' OK!" %globaldatabase)
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error, e:
			self.log.error(str(e))
			return False
		self.log.info("==> connect and operate mysql finished!")
		return True

	def configMysql(self):
		host = self.configParser.get("mysql", "ip")
		user = self.configParser.get("mysql", "username")
		passwd = self.configParser.get("mysql", "password")
		port = self.configParser.getint("mysql", "port")
		db = self.configParser.get("mysql", "database")
		return self._configMysql(host=host, user=user, passwd=passwd, port=port, db=db)

	def registerPaysys(self, name, passwd):
		self.log.info("================================================")
		ora_ip = self.configParser.get("paysys", "ip")
		ora_port = self.configParser.get("paysys", "listen_port")
		ora_server_name = self.configParser.get("paysys", "server_name")
		ora_dsn = cx_Oracle.makedsn(ora_ip, ora_port, ora_server_name)
		username = self.configParser.get("paysys", "manage_user")
		password = self.configParser.get("paysys", "manage_passwd")
		self.log.info("==> register local machine to paysys(%s:%s/%s)" %(ora_ip, ora_port, ora_server_name))
		self.log.info("register name: %s" %name)
		self.log.info("register passwd: %s" %passwd)
		self.log.info("machine IP: %s" %self.localIp)
		self.log.info("machine MAC: %s" %self.localMac)
		try:
			connection = cx_Oracle.Connection(username, password, ora_dsn)
			cursor = connection.cursor()
			cursor.execute("select max(GATEWAY_ID) from config_gateway")
			format = map(lambda x: int(x[0]), cursor.fetchall())
			if not self._checkYesOrNO("please use caution! are you sure?(y/N):"):
				cursor.close()
				connection.close()
				self.log.info("user cancelled!!!")
				return False
			if len(format) > 0:
				md5 = hashlib.md5()
				md5.update(passwd.encode('utf-8'))
				md5pd = md5.hexdigest().upper()
				sql = """insert into config_gateway(GATEWAY_ID, GATEWAY_NAME, ZONE_ID, PASSWORD, IP, MAC, STATE, RELAY_IP, DESCRIPTION)
					values(%d, '%s', 1, '%s', '%s', '%s', 0, '%s', 'insert by AutoConfig')"""
				cursor.execute(sql %(int(format[0]) + 1, name, md5pd, self.localIp, self.localMac, self.localIp))
			else:
				cursor.close()
				connection.close()
				self.log.error("can not get max(gateway_id) value")
				return False
			connection.commit()
			cursor.close()
			connection.close()
		except Exception, e:
			self.log.error(str(e))
			return False
		self.log.info("add one record to paysys ...")
		self.log.info("==> register paysys gateway success !!!")
		return True

def main():
	#check python version
	if sys.version_info[0] > 2:
		print("The python version is %d.%d. But python 2.x is required. (Version 2.7 is well tested)\n"
			"Download it here: https://www.python.org/" % (sys.version_info[0], sys.version_info[1]))
		raw_input("\nplease input any key exit...")
		return False

	#check parameters type
	parser = OptionParser(usage="\n  %%prog <Options> [config] [log]\n  notice: please configurate [%s] at first\n  e.g: %%prog -c -s" %RC_CONFIG_FILE)
	parser.add_option(
		"-p", "--packlibrary", action="store_true", dest="p", help="jv2 program and runtime librarys packaged")
	parser.add_option(
		"-c", "--client", action="store_true", dest="c", help="jv2 client automatic configuration")
	parser.add_option(
		"-s", "--server", action="store_true", dest="s", help="jv2 server automatic configuration")
	parser.add_option(
		"-t", "--router", action="store_true", dest="t", help="jv2 router automatic configuration")
	parser.add_option(
		"-r", "--registerpaysys", action="store_true", dest="r", help="automatic register machine to paysys")
	parser.add_option(
		"-m", "--operatemysql", action="store_true", dest="m", help="connect mysql and check version, create user table")
	opts, args = parser.parse_args()
	if not opts.p and not opts.c and not opts.s and not opts.t and not opts.r and not opts.m:
		parser.print_help()
		return False

	if opts.s and opts.r:
		parser.error("options -s and -r are mutually exclusive") 
		return False

	if opts.s and opts.m:
		parser.error("options -s and -r are mutually exclusive") 
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

	if opts.r:
		reg_name = raw_input("please input register name:")
		reg_passwd = raw_input("please input register passwd:")
		config.checkIpCorrectness()
		config.checkMacCorrectness()
		config.registerPaysys(reg_name, reg_passwd)
	if opts.m:
		config.configMysql()
	if opts.p:
		config.packLibrary(RC_COMMON_PACK)
	if opts.c:
		config.checkIpCorrectness()
		config.configClient()
	if opts.s:
		config.checkIpCorrectness()
		config.checkMacCorrectness()
		config.configServer()
	if opts.t:
		config.configRouter()

	raw_input("\nplease input any key exit...")

if __name__ == '__main__':
	main()