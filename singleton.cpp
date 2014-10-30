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
		DeleteCriticalSection(&m_CriticalSetion);
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
};
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
protected:
    singleton(){}
    virtual ~singleton(){}
	static T* m_pInst;
	static CMutex m_Mutex;

private:
	class C1234567
	{
	    ~C1234567()
	    {
	        delete m_pInst;
	        m_pInst = NULL;
	    }
	};
	static C1234567 m_C1234567;
};

template<typename T> T* singleton<T>::m_pInst = NULL;
template<typename T> CMutex singleton<T>::m_Mutex;
template<typename T> typename singleton<T>::C1234567 singleton<T>::m_C1234567;

#include <stdio.h>
#include <stdlib.h>
#ifndef _WIN32
#include <unistd.h>
#endif

class CTest : public singleton<CTest>
{
public:
	CTest()
	{
		m_pVec = new char[1000];
	}
	~CTest()
	{
		delete[] m_pVec;
		printf("----------CTest destruct-----------\n");
	}
	void print()
	{
		printf("CTest call print()\n");
	}
private:
	char* m_pVec;
};

// 可重入函数
void* work(void * arg)
{
	CTest* p = CTest::GetInstance();
	if (p)
	{
		printf("CTest pointer = %p\n", p);
		p->print();
	}

	return NULL;
}

int main(int argc, char* argv[])
{
    const int MAX_COUNT = 10;
#ifndef _WIN32
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
#else
	HANDLE hThread[MAX_COUNT];
	for (int i = 0; i < MAX_COUNT; i++)
	{
		hThread[i] = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)work, NULL, 0, NULL);
		printf("create thread id = %d\n", hThread[i]);
	}
	WaitForMultipleObjects(MAX_COUNT, hThread, TRUE, INFINITE);
#endif

    return 0;
}



