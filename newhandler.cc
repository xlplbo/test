#include <iostream>
#include <new>
#include <cstdio>
#include <cstdlib>

namespace std
{
  typedef void (*new_handler)();
  new_handler set_new_handler(new_handler p) throw();
};

void OutofMemory()
{
  char szBuff[128] = "";
  snprintf(szBuff, sizeof(szBuff), "%s:out of memory!!!", __FUNCTION__);
  std::cout << szBuff << std::endl;
  std::abort();
}

//RAII class
class NewHolder 
{
public:
  explicit NewHolder(std::new_handler nh)
    : handler(nh)
  {}
  ~NewHolder()
  {
    std::set_new_handler(handler);
  }
private:
  std::new_handler handler;
  NewHolder(const NewHolder&);
  NewHolder& operator=(const NewHolder&);
};

//New Handler Support class
template<typename T>
class NewSupport
{
public:
  static std::new_handler set_new_handler(std::new_handler p) throw();
  static void* operator new(std::size_t size) throw(std::bad_alloc);
  static void* operator new[](std::size_t size) throw(std::bad_alloc);
private:
  static std::new_handler currentHandler;
};

template<typename T>
std::new_handler NewSupport<T>::set_new_handler(std::new_handler p) throw()
{
  std::new_handler oldHandler = currentHandler;
  currentHandler = p;
  return oldHandler;
}

template<typename T>
void* NewSupport<T>::operator new(std::size_t size) throw(std::bad_alloc)
{
  NewHolder h(std::set_new_handler(currentHandler));
  return ::operator new(size);
}

template<typename T>
void* NewSupport<T>::operator new[](std::size_t size) throw(std::bad_alloc)
{
  NewHolder h(std::set_new_handler(currentHandler));
  return ::operator new [](size);
}

template<typename T>
std::new_handler NewSupport<T>::currentHandler = NULL;

class Test : public NewSupport<Test>
{
public:
  Test()
  {
    //p = new int[10000000000L];
  }
  ~Test()
  {
    //delete p;
    //p = NULL;
  }
  void print()
  {
    std::cout << "Test Class print()!!!" << std::endl;
  }
private:
  int* p;
};

int main(int argc, char* argv[])
{
  // 设置全局的handler
  //  std::set_new_handler(OutofMemory);
  //  int* p = new int[10000000000L];
  //  delete p;
  
  // 设置class Test的handler
  //  Test::set_new_handler(OutofMemory);
  //  Test* p = new Test[10000000000L];
  
  // 看看在哪里handler了
  //  Test::set_new_handler(OutofMemory);
  //  Test* p = new Test;
  //  p->print();

  //  delete p;
  return 0;
}
