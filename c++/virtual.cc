#include <stdio.h>
#include <tr1/memory>
#include <tr1/functional>

class GameCharacter 
{
public:
  void healthValue()
  {
    printf("before %s\n", __FUNCTION__);
    doHealthValue();
    printf("after %s\n", __FUNCTION__);
  }
private:
  virtual void doHealthValue()
  {
    printf("GameCharacter doHealthValue\n");
  }
};

class Player : public GameCharacter 
{
private:
  virtual void doHealthValue()
  {
    printf("Player doHealthValue\n");
  }
};

class GameCharacter2;

void defaultHealthCalc(const GameCharacter2& gc)
{
  printf("%s\n", __FUNCTION__);
}

void dogHealthCalc(const GameCharacter2& gc)
{
  printf("%s\n", __FUNCTION__);
}

class GameCharacter2 
{
public:
  typedef void (*HealthCalcFunc)(const GameCharacter2&);
  explicit GameCharacter2(HealthCalcFunc hcf = defaultHealthCalc)
    : m_healthFunc(hcf)
  {}
  void healthValue() const
  {
    m_healthFunc(*this);
  }
private:
  HealthCalcFunc m_healthFunc;
};

class GameCharacter3;

void defaultObjFunc(const GameCharacter3& gc)
{
  printf("%s\n", __FUNCTION__);
}

void dogObjFunc(const GameCharacter3& gc)
{
  printf("%s\n", __FUNCTION__);
}

class GameCharacter3 
{
public:
  //typedef void (*HealthCalcFunc)(const GameCharacter3&);
  typedef std::tr1::function<void (const GameCharacter3&)> ObjFunc;
  explicit GameCharacter3(ObjFunc hcf = defaultObjFunc)
    : m_healthFunc(hcf)
  {}
  void healthValue() const
  {
    m_healthFunc(*this);
  }
private:
  ObjFunc m_healthFunc;
};

class GameCharacter4;
class CHealthCalc 
{
public:
  virtual int calc(const GameCharacter4& gc) const
  {
    printf("CHealthCalc::%s\n", __FUNCTION__);
  }
};
CHealthCalc defaultCHealthCalc;
class GameCharacter4 
{
public:
  explicit GameCharacter4(CHealthCalc* pChc = &defaultCHealthCalc)
    : pHealthCalc(pChc)
  {}
  int healthValue() const
  {
    return pHealthCalc->calc(*this);
  }
private:
  CHealthCalc* pHealthCalc;
};

int main(int argc, char* argv[])
{
  //NVI手法
  GameCharacter* p = new Player;
  p->healthValue();
  delete p;
  //将virtual函数替换为“函数指针成员变量”
  GameCharacter2 gc1;
  gc1.healthValue();
  GameCharacter2 gc2(dogHealthCalc);
  gc2.healthValue();
  //以tr1::function成员变量替换virtual函数
  GameCharacter3 go1;
  go1.healthValue();
  GameCharacter3 go2(dogObjFunc);
  go2.healthValue();
  //将一个继承体系内的virtual函数替换为另一个继承体系内的virtual函数
  GameCharacter4 gcl1;
  gcl1.healthValue();

  return 0;
}
