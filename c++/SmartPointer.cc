#include <cstdio>
#include <atomic>
 
class CRefCount
{
public:
    CRefCount() : m_nCount(0) {}
    unsigned AddRef() 
    {
      return ++m_nCount;
    }
    unsigned DecRef()
    {
      return --m_nCount;
    }
private:
    CRefCount(const CRefCount&);
    CRefCount& operator =(const CRefCount&);
    std::atomic<unsigned> m_nCount;
};
 
template <class T>
class CSmartPointer
{
public:
    CSmartPointer();
    virtual ~CSmartPointer();

    CSmartPointer(T* ptr);
    CSmartPointer(CSmartPointer<T>& sp);
    CSmartPointer<T>& operator =(T* ptr);
    CSmartPointer<T>& operator =(CSmartPointer<T>& sp);
 
    operator bool();
    T* operator ->();
    T& operator *();    
    T* Get();
    CRefCount* GetRef();

private:
    void Remove();
 
private:
    T*          m_ptr;
    CRefCount*  m_pCountRef;
};
 
template <class T>
CSmartPointer<T>::CSmartPointer()
:m_ptr(NULL)
{
    m_pCountRef = new CRefCount;
    if (m_pCountRef)
        m_pCountRef->AddRef();
}

template <class T>
CSmartPointer<T>::~CSmartPointer()
{
    Remove();
}
 
template <class T>
CSmartPointer<T>::CSmartPointer(T* ptr)
{
  // printf("CSmartPointer<T>::CSmartPointer(T* ptr) %s\n", __FUNCTION__);
    m_ptr = ptr;
    m_pCountRef = new CRefCount;
    if (m_pCountRef)
        m_pCountRef->AddRef();
}
 
template <class T>
CSmartPointer<T>::CSmartPointer(CSmartPointer<T>& sp)
{
  // printf("CSmartPointer<T>::CSmartPointer(CSmartPointer<T>& sp) %s\n", __FUNCTION__);
    m_ptr = sp.Get();
    m_pCountRef = sp.GetRef();
    if (m_pCountRef)
        m_pCountRef->AddRef();
}

template <class T>
CSmartPointer<T> & CSmartPointer<T>::operator =(T* ptr)
{
  // printf("CSmartPointer<T> & CSmartPointer<T>::operator =(T* ptr) %s\n", __FUNCTION__);
    if (m_ptr == ptr)
        return *this;
 
    Remove();
    m_ptr = ptr;
    m_pCountRef = new CRefCount;
    if (m_pCountRef)
        m_pCountRef->AddRef();
 
    return *this;
}

template <class T>
CSmartPointer<T> & CSmartPointer<T>::operator =(CSmartPointer<T>& sp)
{
  //printf("CSmartPointer<T> & CSmartPointer<T>::operator =(CSmartPointer<T>& sp) %s\n", __FUNCTION__);
    if (this == &sp)
        return *this;
 
    Remove();
    m_ptr = sp.Get();
    m_pCountRef = sp.GetRef();
    if (m_pCountRef)
        m_pCountRef->AddRef();
 
    return *this;
}
 
template<class T>
void CSmartPointer<T>::Remove()
{
    if (m_pCountRef && m_pCountRef->DecRef() <= 0)
    {
        delete m_ptr;
        m_ptr = NULL;
        delete m_pCountRef;
        m_pCountRef = NULL;
    }
}
 
template <class T>
CSmartPointer<T>::operator bool()
{
    return (m_ptr != NULL);
}
 
template <class T>
T*  CSmartPointer<T>::operator->()
{
    return m_ptr;
}
 
template <class T>
T&  CSmartPointer<T>::operator *()
{
    return *m_ptr;
}
 
template <class T>
T* CSmartPointer<T>::Get()
{
    return m_ptr;
}
 
template<class T>
CRefCount* CSmartPointer<T>::GetRef()
{
    return m_pCountRef;
}
 
struct MyStruct
{
    int a;
    int b;
    MyStruct() : a(0), b(0)
    {
       printf("MyStruct structure!\n");
    }
    ~MyStruct()
    {
       printf("MyStruct destructor! a = %d, b = %d\n", a, b);
    }
    void print()
    {
       printf("MyStruct print() a = %d, b = %d\n", a, b);
   }
};
 
//测试智能指针
void test_SmartPointer()
{
    CSmartPointer<MyStruct> ms1(new MyStruct);
    if (ms1)
    {
        ms1->a = 10;
        ms1->b = 20;
        ms1->print();
    }
 
    CSmartPointer<MyStruct> ms2;
    ms2 = ms1;
    if (ms2)
    {
        ms2->a = 100;
        ms2->b = 200;
        ms2->print();
    }
 
    CSmartPointer<MyStruct> ms3(ms2);
    if (ms3)
    {
        ms3->a = 1000;
        ms3->b = 2000;
        ms3->print();
    }
    ms3 = new MyStruct;
    if (ms3)
    {
        ms3->a = 3000;
        ms3->b = 4000;
        ms3->print(); 
    }

}
 
int main(int argc, char* argv[])
{
    test_SmartPointer();//函数调用是为了在main退出之前就能看到指针被释放。
 
    //system("PAUSE");
    return 0;
}
