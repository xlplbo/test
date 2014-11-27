#include <stdio.h>
#include <process.h>
#include <windows.h>
/* volatile防止编译器优化，强制从内存读取变量
 * Interlocked系列函数的使用
 * 多线程切换时会保存现场，出现计数不正确是因为多线程重复写的问题
 */
volatile long g_nLoginCount; //登录次数
unsigned int __stdcall Fun(void *pPM); //线程函数
const DWORD THREAD_NUM = 64;//启动线程数

DWORD WINAPI ThreadFun(void *pPM)
{
	Sleep(100); //some work should to do
	//g_nLoginCount++;
	InterlockedIncrement((LPLONG)&g_nLoginCount);  
	Sleep(50);
	return 0;
}

int main()
{
	//重复20次以便观察多线程访问同一资源时导致的冲突
	int num= 20;
	while (num--)
	{	
		g_nLoginCount = 0;
		int i;
		HANDLE  handle[THREAD_NUM];
		for (i = 0; i < THREAD_NUM; i++)
			handle[i] = CreateThread(NULL, 0, ThreadFun, NULL, 0, NULL);
		WaitForMultipleObjects(THREAD_NUM, handle, TRUE, INFINITE);
		printf("有%d个用户登录后记录结果是%d\n", THREAD_NUM, g_nLoginCount);
	}
	getchar();
	return 0;
}