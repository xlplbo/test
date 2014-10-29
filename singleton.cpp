/*************************************************************************
    > File Name: singleton.cpp
    > Author: xlplbo
    > Mail: booxlp@gmail.com
    > Created Time: Wed 29 Oct 2014 07:01:29 AM PDT
 ************************************************************************/

#ifdef _WIN32
#include <windows.h>
#include <process.h>
#define barrier() NULL
class CMutex
{
public:
	CMutex()
	{
		InitializeCriticalSection(&m_CriticalSetion);
	}
	~CMutex()
	{
		DeleteCriticalSectioin(&m_CriticalSetion);
	}
	bool Lock()
	{
		EnterCriticalSection(&m_CriticalSetion);
		return true;
	}
	bool Unlock()
	{
		LeaveCriticalSection(&m_CriticalSetion);
		return true;
	}
private:
	CRITICAL_SECTION m_CriticalSetion;
}
#else
#include <pthread.h>
#define barrier() __asm__ __volatile__("":::"memory")
class CMutex
{
public:
	CMutex()
	{
		pthread_mutex_init(&m_Mutex, NULL);
	}
	~CMutex()
	{
		pthread_mutex_destroy(&m_Mutex);
	}
	bool Lock()
	{
		return pthread_mutex_lock(&m_Mutex) == 0;
	}
	bool Unlock()
	{
		return pthread_mutex_unlock(&m_Mutex) == 0;
	}
private:
	pthread_mutex_t m_Mutex;
};
#endif

template <typename T>
class singleton
{
public:
	static T* GetInstance()
	{
		if (!m_pInst)
		{
			m_Mutex.Lock();
			if (!m_pInst)
			{
				T* p = new T;
				barrier(); //barrier()执行完成之前内存被初始化
				m_pInst = p;
			}
			m_Mutex.Unlock();
		}
		return m_pInst;
	}
	~singleton()
	{
		delete m_pInst;
		m_pInst = NULL;
	}
private:
	singleton();
	static T* m_pInst;
	static CMutex m_Mutex;
};

template<typename T> T* singleton<T>::m_pInst = NULL;

template<typename T> CMutex singleton<T>::m_Mutex;

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

class CTest
{
public:
	void print()
	{
		printf("CTest call print()\n");
	}
};

// 可重入函数
void* work(void * arg)
{
	CTest* p = (CTest*)singleton<CTest>::GetInstance();
	if (p)
	{
		printf("CTest pointer = %p\n", p);
		p->print();
	}
	sleep(5);
	return NULL;
}

int main(int argc, char* argv[])
{
	const int MAX_COUNT = 10;
	pthread_t p_id[MAX_COUNT];
	for (int i = 0; i < MAX_COUNT; i ++)
	{
		if (pthread_create(&p_id[i], NULL, work, NULL) != 0)
		{
			perror("pthread_create");
			exit(0);
		}
		printf("create thread id = %d\n", p_id[i]);
	}
	for (int i = 0; i < MAX_COUNT; i ++)
		pthread_join(p_id[i], NULL);
	return 1;
}



