1.autoconfig����ʲô�ģ�
autoconfig��һ����Խ���Խ�ϰ���Զ������ó�����Ҫ�����У�
���ÿͻ��ˣ�cmd: autoconfig.exe -c [config.ini] [logfilename]
���÷�������cmd: autoconfig.exe -s [config.ini] [logfilename]
���ÿ���������� cmd: autoconfig.exe -t [config.ini] [logfilename]
����MYSQL���ݿⲢ������ɫ�� cmd: autoconfig.exe -m [config.ini] [logfilename]
һ��ע�����ص�Paysys��cmd: auotconfig.exe -r [config.ini] [logfilename]
�Զ�������п�ͳ���cmd: auotconfig.exe -p [config.ini] [logfilename]

2.autoconfig����˵��
ʹ��Option����-h����--help���鿴����ʹ�ð���
[]��ʾ��ѡ���������ʹ�ú�����ʹ��Ĭ�������ļ�������Ĭ����־�ļ�������cmd: autoconfig.exe -cʹ�õ�����Ϊconfig.ini,���ɵ���־�ļ�Ϊautoconfig.log
Option����-s��-m��-r����ͬʱʹ�ã�����-c��-s��ͬʱʹ�ã�����cmd: autoconfig.exe -c -s�Զ����ÿͻ��˺ͷ�����
Option����-p,��ָ��Ŀ¼�µ����п�ͳ�������data.zip,����������ʹ�á�һ���ǳ���Գʹ�õģ�����С�������ԣ���������κ���������ʣ�����ϵrtx:liubo5

3.�����ļ�config.ini˵��
[client] ���ÿͻ�����Ҫʹ�õ�section
[server] ���÷�������Ҫʹ�õ�section��������[mysql]��[paysys]
[packlibrary] ������п�ͳ�����Ҫʹ�õ�section
[mysql] ���ý�ɫ���ݿ�ʹ�õ�section
[paysys] �Զ�ע�����ܵ�paysys��Ҫʹ�õ�section
[router] ���ÿ����������Ҫʹ�õ�section

4.��������
����������ȱ������Խ�����ļ�
Bishop�޷�������paysys��֤ʧ�ܣ������޷�����ʱ��ͬ��
������Ĭ�������ڱ�������������������������ֶ�����Ŀ�������IP��ַ
��Ҫ����ʹ��ע�����ܵ�paysys���ܣ��ᵼ�ºܶ��������ݼ�¼

--------------------------------------�����ķָ��ߣ��������ݷǳ���Գ����--------------------------------------------------

5.autoconfigԴ��ṹ˵��
autoconfig.py���߹���ʵ�ֽű�
setup.py���ű������exe��ִ���ļ����ýű�
config.ini����ʹ�õ������ļ�
oci.dllע��paysysʱ����oracle��Ҫ��dll
oraocci10.dllע��paysysʱ����oracle��Ҫ��dll
oraociei10.dllע��paysysʱ����oracle��Ҫ��dll
ReadMe.txt����˵���ĵ���С���ʹ��ǰһ��Ҫ��
windll.zip�Ѵ���õ�windows���п�

6.��ν�autoconfigԴ������exe��ִ���ļ�
��װpython2.7.*�汾���������Ʋ�https://www.python.org/downloads/
����python��������,��C:\Python27;C:\Python27\Scripts��ӵ�PATH
��װpython��������pip,�ο�http://www.cnblogs.com/linn/p/3858009.html
��װ�������py2exe���Ʋ�http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe/download
�ڹ���Ŀ¼������python setup.py py2exe,���ȱ��ģ�鱨����ʹ�� pip install modelname��װģ������������
����ɹ����ɵ�distĿ¼���������Ĺ���Ŀ¼

7.������֧�ִ��ļ�Ŀ¼������ݷ�ʽ������Ŀǰ����֧�֣��ѱ�����
