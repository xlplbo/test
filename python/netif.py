#!/usr/bin/python
# coding:utf-8
# import netifaces

def _getLocalIp(self):
    import sys
    import socket
    if sys.platform == 'win32':
        return socket.gethostbyname(socket.gethostname())
    if sys.platform.startswith('linux'):
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
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:].upper()
    return "%s-%s-%s-%s-%s-%s" %(mac[:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])

# def _getNetInterface(self):
#     import netifaces
#     for dev in netifaces.interfaces():
#         infos = netifaces.ifaddresses(dev)
#         if len(infos) < 2:
#             continue
#         ip = infos[netifaces.AF_INET][0]['addr']
#         mac = infos[netifaces.AF_LINK][0]['addr']
#         if len(ip) > 0 and ip != "127.0.0.1" and len(mac) > 0:
#             return (ip, mac.upper().replace(":", "-"))
#     return None

import os

def getdirsize(dir):
    size = 0L
    for root, dirs, files in os.walk(dir):
        print root, dirs, files, files.__len__()
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size/1024/1024

print getdirsize("C:\Users\liubo5\Desktop\\test\\autoconfig")

# blacklist = [".svn", "abc"]
# root = ["asdfasfasfds", "rgweorjo"]
# print [x for x in blacklist for y in root if x in y]

# import hashlib
# passwd = "a"
# m = hashlib.md5()
# m.update(passwd.encode('utf-8'))
# print m.hexdigest()

# -*- coding: cp936 -*- # 
import os
import pythoncom
from win32com.shell import shell
#from win32com.shell import shellcon

# def set_shortcut(filename,lnkname):#如无需特别设置图标，则可去掉iconname参数
#     shortcut = pythoncom.CoCreateInstance(
#     shell.CLSID_ShellLink, None,
#     pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
#     shortcut.SetPath(filename)
#     if os.path.splitext(lnkname)[-1] != '.lnk':  
#         lnkname += ".lnk" 
#     shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname,0)
    
# if __name__ == "__main__":
#     set_shortcut("C:\\Users\\liubo5\\Desktop\\test\\autoconfig","C:\\Users\\liubo5\\Desktop\\test\\data")

s = "er"
print s, len(s)