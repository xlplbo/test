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
import socket
import MySQLdb
import cx_Oracle
import uuid
import time

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

class AutoConfig(object):
	"""docstring for AutoConfig"""
	def __init__(self, config, log):
		super(AutoConfig, self).__init__()
		self.progress = 0
		self.paysys_regname = time.strftime('CP%Y%m%d%H%M%S',time.localtime(time.time()))
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

	def _getLocalMac(self):
		node = uuid.getnode()
		mac = uuid.UUID(int = node).hex[-12:]
		return mac

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

	def _showProgress(self, step):
		self.progress += 1
		if step > 0:
			index = self.progress // step
			if index <= 10 and index * step == self.progress:
				self.log.info("progress %d%%" %(index*10))

	def _handlerError(self, func, path, excinfo):
		os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
		func(path)
		self.log.info("Exception handling: %s %s" %(getattr(func, '__name__'), path))

	def _removeFileOrDir(self, path):
		if os.path.exists(path):
			if os.path.isdir(path):
				shutil.rmtree(path, False, self._handlerError)
			else:
				os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
				os.remove(path)
			self.log.info("remove '%s' ..." %path)

	def _makeDir(self, path):
		try:
			self._removeFileOrDir(path)
			os.makedirs(path)
			self.log.info("mkdir '%s' ..." %path)
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
		for v in os.listdir("."):
			if os.path.isfile(v) and v == name and \
			self._checkYesOrNO("check file '%s' is exist! do you update this file?(y/N):" %name):
				self._removeFileOrDir(name)
				break
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
		if not os.path.isdir(path):
			return
		for name in os.listdir(path):
			if '.svn' in name:
				continue
			childdir = os.path.join(path, name)
			if not os.path.isdir(childdir):
				filedict[childdir] = name
			else:
				self._getTreeDict(childdir, filedict) 

	def _copyFile(self, srcname, dstname, step = 0):
		try:
			self._removeFileOrDir(dstname)
			if os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isfile(srcname):
				shutil.copy2(srcname, dstname)
		except Exception, e:
			self.log.error(str(e))
		shutil.copystat(srcname, dstname)
		self._showProgress(step)

	def _copyFolder(self, src, dst, blacklist, step = 0):
		if not os.path.isdir(src):
			return
		if not os.path.exists(dst):
			os.mkdir(dst)
		for name in os.listdir(src):
			if name.strip() in blacklist:
				continue
			srcname = os.path.join(src, name)
			dstname = os.path.join(dst, name)
			if not os.path.isdir(srcname):
				self._copyFile(srcname, dstname, step)
			else:
				self._copyFolder(srcname, dstname, blacklist, step)

	def copyFolder(self, src, dst, blacklist = []):
		if not os.path.exists(src):
			self.log.error("can not find '%s', please check '%s' file" %(src, self.config))
		if not os.path.exists(dst):
			self.log.error("can not find '%s', please check '%s' file" %(dst, self.config))
		self.log.info("copy floders '%s' to '%s' ..." %(src, dst))
		filedict = {}
		self._getTreeDict(src, filedict)
		step = (len(filedict) - (len(filedict) % 10)) // 10
		self.progress = 0
		blacklist.append(".svn")
		self._copyFolder(src, dst, map(lambda s: s.lower(), blacklist), step)
		self.log.info("actually %d file(s) have been copied" %self.progress)

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

	def _parseIniFile(self, root, filename, func):
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
		func(filepath)
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
			serverip = self._getLocalIp()
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
		if self._isLinux() and not self._checkYesOrNO("do you config client on linux OS?(y/N):"):
			self.log.info("config client on linux OS cancel by user!")
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
		localIp = self._getLocalIp()
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Version')
		parser.set('Version', 'Version', 2)
		parser.add_section('KG_Goddess')
		parser.set('KG_Goddess', 'ListenIP', localIp)
		parser.set('KG_Goddess', 'ListenPort', 5001)
		parser.set('KG_Goddess', 'LoopSleepTime', 10)
		parser.set('KG_Goddess', 'AutoDisconnectTime', 120000)
		parser.set('KG_Goddess', 'SendRecvTimeout', 60000)
		parser.set('KG_Goddess', 'Group', 1)
		parser.set('KG_Goddess', 'MaxRoleCountInAccount', 9)
		parser.add_section('DatabaseServer')
		parser.set('DatabaseServer', 'Server', self.configParser.get("server", "mysql_ip"))
		parser.set('DatabaseServer', 'UserName', self.configParser.get("server", "mysql_username"))
		parser.set('DatabaseServer', 'Database', self.configParser.get("server", "mysql_database"))
		parser.set('DatabaseServer', 'Password', self.configParser.get("server", "mysql_password"))
		parser.set('DatabaseServer', 'EnableEncrypt', 0)
		parser.add_section('RoleStatistic')
		parser.set('RoleStatistic', 'ListenIP', localIp)
		parser.set('RoleStatistic', 'ListenPort', 6001)
		parser.set('RoleStatistic', 'SendRecvTimeout', 60000)
		with file(path, 'w') as f:
   			parser.write(f)

   	def _parseBishopConfig(self, path):
   		localIp = self._getLocalIp()
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Version')
		parser.set('Version', 'Version', "bishop2")
		parser.add_section('Paysys')
		parser.set('Paysys', 'IPAddress', self.configParser.get("server", "paysys_ip"))
		parser.set('Paysys', 'Port', self.configParser.get("server", "paysys_port"))
		parser.set('Paysys', 'UserName', self.configParser.get("server", "paysys_username"))
		parser.set('Paysys', 'Password', self.configParser.get("server", "paysys_password"))
		parser.set('Paysys', 'SendRecvTimeout', 60000)
		parser.set('Paysys', 'ReconnectTime', 10000)
		parser.set('Paysys', 'LoopTime', 100)
		parser.set('Paysys', 'PingTime', 10000)
		parser.add_section('Goddess')
		parser.set('Goddess', 'IPAddress', localIp)
		parser.set('Goddess', 'LocalIPAddress', localIp)
		parser.set('Goddess', 'Port', 5001)
		parser.set('Goddess', 'SendRecvTimeout', 60000)
		parser.set('Goddess', 'ReconnectTime', 10000)
		parser.set('Goddess', 'LoopTime', 100)
		parser.set('Goddess', 'PingTime', 20000)
		parser.add_section('Relay')
		parser.set('Relay', 'LocalIPAddress', localIp)
		parser.set('Relay', 'OpenPort', 5632)
		parser.set('Relay', 'SendRecvTimeout', 60000)
		parser.set('Relay', 'LoopTime', 100)
		parser.set('Relay', 'PingTime', 20000)
		parser.set('Relay', 'AccountInRelayTimeout', 60000)
		parser.add_section('GameServer')
		parser.set('GameServer', 'LocalIPAddress', localIp)
		parser.set('GameServer', 'OpenPort', 5633)
		parser.set('GameServer', 'SendRecvTimeout', 180000)
		parser.set('GameServer', 'AccountInManagerTimeout', 300000)
		parser.set('GameServer', 'LoopTime', 100)
		parser.set('GameServer', 'PingTime', 60000)
		parser.add_section('Player')
		parser.set('Player', 'LocalIPAddress', localIp)
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
   		localIp = self._getLocalIp()
   		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Gmc')
		parser.set('Gmc', 'Address', self.configParser.get("server", "paysys_ip"))
		parser.set('Gmc', 'LocalAddr', localIp)
		parser.set('Gmc', 'Port', 9991)
		parser.set('Gmc', 'Enable', 0)
		parser.set('Gmc', 'EncryptionType', 0)
		parser.set('Gmc', 'ReConnInterval', 20000)
		parser.set('Gmc', 'PingInterval', 90000)		
		parser.add_section('Bishop')
		parser.set('Bishop', 'Address', localIp)
		parser.set('Bishop', 'LocalAddr', localIp)
		parser.set('Bishop', 'Port', 5632)
		parser.set('Bishop', 'Enable', 1)
		parser.set('Bishop', 'EncryptionType', 0)
		parser.set('Bishop', 'ReConnInterval', 20000)
		parser.set('Bishop', 'PingInterval', 90000)
		parser.add_section('Goddess')
		parser.set('Goddess', 'Address', localIp)
		parser.set('Goddess', 'LocalAddr', localIp)
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
		parser.set('Host', 'LocalAddr', localIp)
		parser.set('Host', 'ListenPort', 5003)
		parser.set('Host', 'SendRecvTimeout', 60000)
		parser.set('Host', 'LoopTime', 50)
		parser.set('Host', 'PingTime', 60000)
		parser.set('Host', 'PlayerCnt', 10)
		parser.set('Host', 'Precision', 1)
		parser.set('Host', 'FreeBuffer', 15)
		parser.set('Host', 'BufferSize', 1048576)
		parser.add_section('Chat')
		parser.set('Chat', 'LocalAddr', localIp)
		parser.set('Chat', 'ListenPort', 5004)
		parser.set('Chat', 'SendRecvTimeout', 60000)
		parser.set('Chat', 'LoopTime', 50)
		parser.set('Chat', 'PlayerCnt', 10)
		parser.set('Chat', 'Precision', 1)
		parser.set('Chat', 'FreeBuffer', 15)
		parser.set('Chat', 'BufferSize', 409600)
		parser.add_section('Tong')
		parser.set('Tong', 'LocalAddr', localIp)
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
		parser.set('DataBase', 'DBHost', self.configParser.get("server", "mysql_ip"))
		parser.set('DataBase', 'DBName', self.configParser.get("server", "mysql_database"))
		parser.set('DataBase', 'LogDBName', "%s_log" %self.configParser.get("server", "mysql_database"))
		parser.set('DataBase', 'DBUser', self.configParser.get("server", "mysql_username"))
		parser.set('DataBase', 'DBPwd', self.configParser.get("server", "mysql_password"))
		parser.set('DataBase', 'DBGroup',1 )
		parser.set('DataBase', 'DBPort', 3306)
		parser.set('DataBase', 'EnableEncrypt', 0)
		parser.add_section('GlobalDatabase')
		parser.set('GlobalDatabase', 'Server', self.configParser.get("server", "mysql_ip"))
		parser.set('GlobalDatabase', 'Database', "jx2vn_global_db")
		parser.set('GlobalDatabase', 'User', self.configParser.get("server", "mysql_username"))
		parser.set('GlobalDatabase', 'Password', self.configParser.get("server", "mysql_password"))
		parser.set('GlobalDatabase', 'Port', 3306)
		parser.set('GlobalDatabase', 'EnableEncrypt', 0)
		parser.add_section('MyGlbDB')
		parser.set('MyGlbDB', 'Server', self.configParser.get("server", "mysql_ip"))
		parser.set('MyGlbDB', 'Database', "jx2vn_global_db")
		parser.set('MyGlbDB', 'User', self.configParser.get("server", "mysql_username"))
		parser.set('MyGlbDB', 'Password', self.configParser.get("server", "mysql_password"))
		parser.set('MyGlbDB', 'Port', 3306)
		parser.set('MyGlbDB', 'EnableEncrypt', 0)
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

	def _configGateway(self, name, root, resource, catalog, func):
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
		specialpath = os.path.join(resource, self.configParser.get("server", "special_catalog"), name)
		if not os.path.isdir(specialpath):
			self.log.error("can not find '%s' path" %specialpath)
			return False
		self.copyFolder(specialpath, dstPath)
		self._extractLibrary(dstPath)
		func(dstPath)
		self.log.info("==> config %s finished!" %name)

	def _parseGamesvr(self, path):
		localIp = self._getLocalIp()
		parser = ConfigParser.ConfigParser()
		parser.optionxform = str
		parser.add_section('Server')
		parser.set('Server', 'ServerCount', 5)
		parser.set('Server', 'ServerIndex', "1,2,3")
		parser.set('Server', 'IS_KINGSOFT_INNER_VERSION_acc_jh34ji84r347e8T56', 0)
		parser.set('Server', 'IS_EXP_SVR', 0)
		parser.set('Server', 'IS_INTERNAL_TEST_SVR', 1)
		parser.add_section('Gateway')
		parser.set('Gateway', 'Ip', localIp)
		parser.set('Gateway', 'Port', 5633)
		parser.add_section('Database')
		parser.set('Database', 'Ip', localIp)
		parser.set('Database', 'Port', 5001)
		parser.add_section('Transfer')
		parser.set('Transfer', 'Ip', localIp)
		parser.set('Transfer', 'Port', 5003)
		parser.add_section('Chat')
		parser.set('Chat', 'Ip', localIp)
		parser.set('Chat', 'Port', 5004)
		parser.add_section('Tong')
		parser.set('Tong', 'Ip', localIp)
		parser.set('Tong', 'Port', 5005)
		parser.add_section('GameServer')
		parser.set('GameServer', 'Port', 6667)
		parser.set('GameServer', 'GM', 1)
		parser.add_section('Net')
		parser.set('Net', 'LocalIP', localIp)
		parser.set('Net', 'ExternalIP', localIp)
		parser.add_section('Overload')
		parser.set('Overload', 'MaxPlayer', 2000)
		parser.set('Overload', 'Precision', 50)
		with file(path, 'w') as f:
   			parser.write(f)

	def _configGameSvr(self, root, resource, catalog):
		name = "GameSvr"
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
		specialpath = os.path.join(resource, self.configParser.get("server", "special_catalog"), name)
		if not os.path.isdir(specialpath):
			self.log.error("can not find '%s' path" %specialpath)
			return False
		self.copyFolder(specialpath, dstPath)
		self._extractLibrary(dstPath)
		self._extractFiles(dstPath, RC_GAMESVR_LIST)
		self._parseIniFile(dstPath, "servercfg.ini", self._parseGamesvr)
		self._removeFileOrDir(os.path.join(dstPath, "dynamic_pwd.ini"))
		self.log.info("==> config %s finished!" %name)

	def _configMysql(self):
		self.log.info("==> connect and operate mysql ...")
		host = self.configParser.get("server", "mysql_ip")
		user = self.configParser.get("server", "mysql_username")
		passwd = self.configParser.get("server", "mysql_password")
		db = self.configParser.get("server", "mysql_database")
		port = self.configParser.getint("server", "mysql_port")
		try:
			conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port)
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
			if db not in format:
				cur.execute('create database if not exists %s' %db)
				self.log.info("create database '%s' ..." %db)
			self.log.info("find database '%s' OK!" %db)
			if "%s_log" %db not in format:
				cur.execute('create database if not exists %s' %("%s_log" %db))
				self.log.info("create database '%s' ..." %("%s_log" %db))
			self.log.info("find database '%s' OK!" %("%s_log" %db))
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error, e:
			self.log.error(str(e))
			return False
		self.log.info("==> connect and operate mysql finished!")
		return True

	def _configPaysys(self):
		ora_ip = self.configParser.get("server", "paysys_ip")
		ora_port = self.configParser.get("server", "ps_listen_port")
		ora_server_name = self.configParser.get("server", "ps_server_name")
		ora_dsn = cx_Oracle.makedsn(ora_ip, ora_port, ora_server_name)
		username = self.configParser.get("server", "ps_manage_user")
		password = self.configParser.get("server", "ps_manage_passwd")
		localIp = self._getLocalIp()
		localMac = self._getLocalMac()
		try:
			connection = cx_Oracle.Connection(username, password, ora_dsn)
			cursor = connection.cursor()
			cursor.execute("create sequence %s" %self.paysys_regname)
			# cursor.execute('select %s.nextval from config_gateway' %self.paysys_regname)
			# format = map(lambda x: int(x[0]), cursor.fetchall())
			# print max(format)
			sql = """insert into config_gateway(GATEWAY_ID, GATEWAY_NAME, ZONE_ID, PASSWORD, IP, MAC, STATE, RELAY_IP, DESCRIPTION) \
				values(%s, '%s', 1, '%s', '%s', '%s', 0, '%s', 'insert by AutoConfig')"""
			print(sql %('%s.nextval' %self.paysys_regname, self.paysys_regname, 'a', localIp, localMac, localIp))	
			cursor.execute(sql %('%s.nextval' %self.paysys_regname, self.paysys_regname, 'a', localIp, "00-21-9B-3A-62-A1", localIp))
			print cursor.fetchall()
			# for x in cursor.fetchall():
			#  	self.log.info(str(x)) 
			# format = map(lambda x: x[0], cursor.fetchall())
			# for x in format:
			# 	cursor.execute("select * from %s" %x)
			# 	print map(lambda x: x[0], cursor.fetchall())
			cursor.execute("drop sequence %s" %self.paysys_regname)
			connection.commit()
			cursor.close()
			connection.close()
		except Exception, e:
			self.log.error(str(e))		

	def configServer(self):
		self.log.info("================================================")
		self.log.info("Prepare to config server!")
		# if not self._configMysql() and not self._checkYesOrNO("mysql operation failed, continue?(y/N):"):
		# 	self.log.info("user cancelled!!!")
		# 	return True
		# return
		# root = self.configParser.get("server", "home").strip()
		# if not self._makeDir(root):
		# 	return False
		# resource = self.configParser.get("server", "resource").strip()
		# if not os.path.isdir(resource):
		# 	self.log.error("can not find '%s', please check '%s' file" %(resource, self.config))
		# 	return False
		# catalog = self.configParser.get("server", "catalog").split(',')
		# self._configGateway("Goddess", root, resource, catalog, self._configGoddess)
		# self._configGateway("Bishop", root, resource, catalog, self._configBishop)
		# self._configGateway("Relay", root, resource, catalog, self._configRelay)
		# self._configGameSvr(root, resource, catalog)
		self._configPaysys()
		self.log.info("==> config server finished!")

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