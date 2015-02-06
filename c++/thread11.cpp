//秒杀多线程第十六篇 多线程十大经典案例之一 双线程读写队列数据
//http://blog.csdn.net/MoreWindows/article/details/8646902
#include <stdio.h>
#include <process.h>
#include <windows.h>
#include <time.h>
const int QUEUE_LEN = 5;
int g_arrDataQueue[QUEUE_LEN];
int g_i, g_j, g_nDataNum;
//关键段 用于保证互斥的在屏幕上输出
CRITICAL_SECTION g_cs;
//信号量 g_hEmpty表示队列中空位 g_hFull表示队列中非空位
HANDLE     g_hEmpty, g_hFull;
//设置控制台输出颜色
BOOL SetConsoleColor(WORD wAttributes)
{
	HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
	if (hConsole == INVALID_HANDLE_VALUE)
		return FALSE;	
	return SetConsoleTextAttribute(hConsole, wAttributes);
}
//读数据线程函数
unsigned int __stdcall ReaderThreadFun(PVOID pM)
{
	int nData = 0;
	while (nData < 20)
	{
		WaitForSingleObject(g_hFull, INFINITE);
		nData = g_arrDataQueue[g_i];
		g_i = (g_i + 1) % QUEUE_LEN;
		EnterCriticalSection(&g_cs);
		printf("从队列中读数据%d\n", nData);
		LeaveCriticalSection(&g_cs);
		Sleep(rand() % 300);
		ReleaseSemaphore(g_hEmpty, 1, NULL);
	}
	return 0;
}
//写数据线程函数
unsigned int __stdcall WriterThreadFun(PVOID pM)
{
	int nData = 0;
	while (nData < 20)
	{
		WaitForSingleObject(g_hEmpty, INFINITE);
		g_arrDataQueue[g_j] = ++nData;
		g_j = (g_j + 1) % QUEUE_LEN;
		EnterCriticalSection(&g_cs);
		SetConsoleColor(FOREGROUND_GREEN);
		printf("    将数据%d写入队列\n", nData);
		SetConsoleColor(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
		LeaveCriticalSection(&g_cs);
		Sleep(rand() % 300);
		ReleaseSemaphore(g_hFull, 1, NULL);
	}
	return 0;
}
int main()
{
	printf("     秒杀多线程第十六篇 多线程十大经典案例 双线程读写队列数据\n");
	printf(" - by MoreWindows( http://blog.csdn.net/MoreWindows/article/details/8646902 ) -\n\n");

	InitializeCriticalSection(&g_cs);
	g_hEmpty = CreateSemaphore(NULL, QUEUE_LEN, QUEUE_LEN, NULL);
	g_hFull = CreateSemaphore(NULL, 0, QUEUE_LEN, NULL);

	srand(time(NULL));
	g_i = g_j = 0;
	HANDLE hThread[2];
	hThread[0] = (HANDLE)_beginthreadex(NULL, 0, ReaderThreadFun, NULL, 0, NULL);
	hThread[1] = (HANDLE)_beginthreadex(NULL, 0, WriterThreadFun, NULL, 0, NULL);

	WaitForMultipleObjects(2, hThread, TRUE, INFINITE);

	for (int i = 0; i < 2; i++)
		CloseHandle(hThread[i]);
	CloseHandle(g_hEmpty);
	CloseHandle(g_hFull);
	DeleteCriticalSection(&g_cs);

	getchar();
	return 0;
}