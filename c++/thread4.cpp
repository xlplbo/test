#include <stdio.h>
#include <process.h>
#include <windows.h>

/* 事件是内核对象
 * 既可以解决同步问题也可以解决互斥访问问题
 */

long g_nNum;
unsigned int __stdcall Fun(void *pPM);
const int THREAD_NUM = 10;
//事件与关键段
HANDLE  g_hThreadEvent; //主线程和子线程同步
CRITICAL_SECTION g_csThreadCode; //子线程之间互斥访问

int main()
{
	//初始化事件和关键段 自动置位,初始无触发的匿名事件
	g_hThreadEvent = CreateEvent(NULL, FALSE, FALSE, NULL); 
	InitializeCriticalSection(&g_csThreadCode);

	HANDLE  handle[THREAD_NUM];	
	g_nNum = 0;
	int i = 0;
	while (i < THREAD_NUM) 
	{
		handle[i] = (HANDLE)_beginthreadex(NULL, 0, Fun, &i, 0, NULL);
		WaitForSingleObject(g_hThreadEvent, INFINITE); //等待事件被触发
		i++;
	}
	WaitForMultipleObjects(THREAD_NUM, handle, TRUE, INFINITE);

	//销毁事件和关键段
	CloseHandle(g_hThreadEvent);
	DeleteCriticalSection(&g_csThreadCode);

	getchar();
	return 0;
}

unsigned int __stdcall Fun(void *pPM)
{
	int nThreadNum = *(int *)pPM; 
	SetEvent(g_hThreadEvent); //触发事件

	Sleep(50);//some work should to do

	EnterCriticalSection(&g_csThreadCode);
	g_nNum++;
	Sleep(0);//some work should to do
	printf("线程编号为%d  全局资源值为%d\n", nThreadNum, g_nNum); 
	LeaveCriticalSection(&g_csThreadCode);
	return 0;
}