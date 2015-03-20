1.autoconfig是做什么的？
autoconfig是一个针对剑二越南版的自动化配置程序，主要功能有：
配置客户端，cmd: autoconfig.exe -c [config.ini] [logfilename]
配置服务器，cmd: autoconfig.exe -s [config.ini] [logfilename]
配置跨服服务器， cmd: autoconfig.exe -t [config.ini] [logfilename]
测试MYSQL数据库并建立角色表， cmd: autoconfig.exe -m [config.ini] [logfilename]
一键注册网关到Paysys，cmd: auotconfig.exe -r [config.ini] [logfilename]
自动打包运行库和程序：cmd: auotconfig.exe -p [config.ini] [logfilename]

2.autoconfig参数说明
使用Option参数-h或者--help，查看工具使用帮助
[]表示可选参数，如果使用忽略则使用默认配置文件和生成默认日志文件，例如cmd: autoconfig.exe -c使用的配置为config.ini,生成的日志文件为autoconfig.log
Option参数-s与-m、-r不能同时使用，但是-c和-s能同时使用，例如cmd: autoconfig.exe -c -s自动配置客户端和服务器
Option参数-p,将指定目录下的运行库和程序打包成data.zip,供其他功能使用。一般是程序猿使用的，其他小伙伴请忽略，如果出现任何问题或疑问，请联系rtx:liubo5

3.配置文件config.ini说明
[client] 配置客户端需要使用的section
[server] 配置服务器需要使用的section，还依赖[mysql]和[paysys]
[packlibrary] 打包运行库和程序需要使用的section
[mysql] 配置角色数据库使用的section
[paysys] 自动注册网管到paysys需要使用的section
[router] 配置跨服服务器需要使用的section

4.常见问题
服务器报错：缺乏部分越南文文件
Bishop无法启动：paysys验证失败，或者无法进行时间同步
服务器默认配置在本机环境，如果不想这样可以手动输入目标机器的IP地址
不要随意使用注册网管到paysys功能，会导致很多无用数据记录

--------------------------------------华丽的分割线，以下内容非程序猿不宜--------------------------------------------------

5.autoconfig源码结构说明
autoconfig.py工具功能实现脚本
setup.py将脚本打包成exe可执行文件配置脚本
config.ini工具使用的配置文件
oci.dll注册paysys时访问oracle需要的dll
oraocci10.dll注册paysys时访问oracle需要的dll
oraociei10.dll注册paysys时访问oracle需要的dll
ReadMe.txt工具说明文档，小伙伴使用前一定要看
windll.zip已打包好的windows运行库

6.如何将autoconfig源码打包成exe可执行文件
安装python2.7.*版本解释器，移步https://www.python.org/downloads/
设置python环境变量,将C:\Python27;C:\Python27\Scripts添加到PATH
安装python包管理器pip,参考http://www.cnblogs.com/linn/p/3858009.html
安装打包工具py2exe，移步http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download
在工具目录下运行python setup.py py2exe,如果缺乏模块报错，请使用 pip install modelname安装模块再重新运行
打包成功生成的dist目录即是完整的工具目录

7.工具已支持大文件目录建立快捷方式，但是目前程序不支持，已被禁用
