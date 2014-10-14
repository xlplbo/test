#include <iostream>
#include <tr1/memory>
#include <boost/scoped_ptr.hpp> //scoped_ptr还不属于tr1
#include <boost/scoped_array.hpp> //scored_array也不属于tr1
#include <boost/shared_array.hpp> //shared_array也不属于tr1

class CTest
{
public:
  CTest() : m_id(0) {}
  CTest(int id) : m_id(id) {}
  ~CTest()
  {
    std::cout << "id :" << m_id << "-Destuctor isbeing called\n";
  }
  void SetId(int id)
  {
    m_id = id;
  }
  int GetId()
  {
    return m_id;
  }
  void DoSomething()
  {
    std::cout << "id :" << m_id << "-DoSomething\n";
  }
private:
  int m_id;
};

int main(int argc, char* argv[])
{
  // scoped_ptr
  boost::scoped_ptr<CTest> pTest(new CTest);
  pTest->SetId(123);
  pTest->DoSomething();
 
  // error scoped_ptr(scoped_ptr const &) is private;
  // boost::scoped_ptr<CTest> pTest2(pTest);
  // error scoped_ptr & operator=(scoped_ptr const &) is private; 
  // boost::scoped_ptr<CTest> pTest2;
  // pTest2 = pTest;
  
  // scoped_array
  boost::scoped_array<CTest> pVecTest(new CTest[2]);
  pVecTest[0].SetId(111);
  pVecTest[0].DoSomething();

  // shared_ptr
  std::tr1::shared_ptr<CTest> pSt(new CTest);
  pSt->SetId(999);
  pSt->DoSomething();

  std::tr1::shared_ptr<CTest> pSt2(pSt); // ok
  pSt2->DoSomething();
  
  std::tr1::shared_ptr<CTest> pSt3; 
  pSt3 = pSt2; // ok
  pSt3->DoSomething();

  // weak_ptr
  std::tr1::weak_ptr<CTest> pWt(pSt);
  std::tr1::shared_ptr<CTest> pWtlock = pWt.lock();
  // pWt->SetId(12345); // error weak_ptr can't used directly
  // pWt->DoSomething(); // error
  pWtlock->SetId(12345);
  pWtlock->DoSomething();

  // shared_array
  boost::shared_array<CTest> pVecSt(new CTest[2]);
  pVecSt[0].SetId(888);
  pVecSt[0].DoSomething();

  // auto_ptr
  std::auto_ptr<CTest> pAt(new CTest);
  pAt->SetId(789);
  pAt->DoSomething();
   
  std::auto_ptr<CTest> pAt2(pAt);
  pAt2->DoSomething();

  std::auto_ptr<CTest> pAt3;
  pAt3 = pAt2;
  pAt3->DoSomething();
  std::cout << "pAt = " << pAt.get() << std::endl; // !!! 
  std::cout << "pAt2 = " << pAt2.get() << std::endl;

  
  return 0;
}
