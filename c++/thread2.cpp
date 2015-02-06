//经典线程同步互斥问题
#include <stdio.h>
#include <process.h>
#include <windows.h>

/* 要解决的两个问题
 * 主线程和子线程的同步问题（i值）
 * 子线程之间的同步问题（g_nNum值）
 */
volatile long g_nNum; //全局资源
unsigned int __stdcall Fun(void *pPM); //线程函数
const int THREAD_NUM = 10; //子线程个数

int main()
{
	g_nNum = 0;
	HANDLE  handle[THREAD_NUM];

	int i = 0;
	while (i < THREAD_NUM) 
	{
		handle[i] = (HANDLE)_beginthreadex(NULL, 0, Fun, &i, 0, NULL);
		i++;//等子线程接收到参数时主线程可能改变了这个i的值
	}
	//保证子线程已全部运行结束
	WaitForMultipleObjects(THREAD_NUM, handle, TRUE, INFINITE);  
	getchar();
	return 0;
}

unsigned int __stdcall Fun(void *pPM)
{
	//由于创建线程是要一定的开销的，所以新线程并不能第一时间执行到这来
	int nThreadNum = *(int *)pPM; //子线程获取参数
	Sleep(50);//some work should to do
	//g_nNum++;  //处理全局资源
	InterlockedIncrement((LPLONG)&g_nNum);
	Sleep(0);//some work should to do
	printf("线程编号为%d  全局资源值为%d\n", nThreadNum, g_nNum);
	return 0;
}