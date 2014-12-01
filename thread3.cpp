#include <stdio.h>
#include <process.h>
#include <windows.h>

/* CRITICAL_SECTION有线程所有权
 * 拥有该临界区的线程可多次进入，故不能解决线程同步问题
 * 不同的线程可以互斥访问
 */


long g_nNum;
unsigned int __stdcall Fun(void *pPM);
const int THREAD_NUM = 10;

//关键段变量声明
CRITICAL_SECTION  g_csThreadParameter, g_csThreadCode;

int main()
{
	//关键段初始化
	InitializeCriticalSection(&g_csThreadParameter);
	InitializeCriticalSection(&g_csThreadCode);

	HANDLE  handle[THREAD_NUM];	
	g_nNum = 0;	
	int i = 0;
	while (i < THREAD_NUM) 
	{
		EnterCriticalSection(&g_csThreadParameter);//进入子线程序号关键区域
		handle[i] = (HANDLE)_beginthreadex(NULL, 0, Fun, &i, 0, NULL);
		++i;
	}
	WaitForMultipleObjects(THREAD_NUM, handle, TRUE, INFINITE);

	DeleteCriticalSection(&g_csThreadCode);
	DeleteCriticalSection(&g_csThreadParameter);

	getchar();
	return 0;
}
unsigned int __stdcall Fun(void *pPM)
{
	int nThreadNum = *(int *)pPM; 
	LeaveCriticalSection(&g_csThreadParameter);//离开子线程序号关键区域

	Sleep(50);//some work should to do

	EnterCriticalSection(&g_csThreadCode);//进入各子线程互斥区域
	g_nNum++;
	Sleep(0);//some work should to do
	printf("线程编号为%d  全局资源值为%d\n", nThreadNum, g_nNum);
	LeaveCriticalSection(&g_csThreadCode);//离开各子线程互斥区域
	return 0;
}