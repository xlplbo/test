1,视C++为一种语言联邦，大致分为4个部分：
A）C。说到底C++仍是以C为基础。区块、语句、预处理器、内置数据类型、数组、指针等等统统来自C。
B）Object-Oriented C++。这部分也就是C with Classes说诉求的：classes(包括构造函数和虚构函数)、封装、继承、多态，虚函数等等。
C）Template C++。这是C++的范型编程部分，tamplates威力强大，它给我们带来了崭新的编程范型，也就是所谓的TMP模板元编程。
D）STL。STL是个template程序库，它对容器、迭代器、算法以及函数对象的规范有极佳的紧密配合与协调，然后template及程序库也可以其他想法建置出来。

2,尽量使用const，enum，inline代替#define
A）#define不被视为语言的一部分，属于预处理指令，编译不会计入符号表无法调试。
B）#define在预处理器处理阶段只做简单的替换，这将带来很多预期意外的行为。
如#define MAX(a, b) ((a)>(b)?(a):(b))
尽管上述宏定义已将变量用括号括起来了，但是还是不能避免MAX(++a, b+10)这样给a所带来的两次不是预期内的自增行为。以为替换为：
Template<typename T>
inline T Max(const T& a, const T& b)
{
return a > b ? a : b;
}
3,尽可能使用const
A)修饰指针
char* p = “hello” //non-const pointer, non-const data
const char* p = “hello” //non-const pointer, const data
char* const p = “hello” //const pointer,non-const data
const char* const p = “hello’ //const pointer, const data
B)修饰迭代器
const std::vector<int>::iterator it = vec.begin(); //const pointer,non-const data
*it = 10 ; //no problem
it ++; //error
std ::vector<int>::const_iterator it = vec.begin() //non-pointer, const data
*it = 10; // error
it ++; //no problem
C)修饰函数参数、返回值、成员函数
class TextBlock {
public:
const char& operator[](std::size_t pos) const
{
return text[pos];
}
char & operator[](std::size_t pos)
{
return const_cast<char&>(static_cast<const TextBlock&>(*this)[pos]);
}
private:
char text[32];
};
4,确定对象被使用前已被初始化
A)区变量初始化和变量赋值两者之间的区别
B)警惕在C++中类未初始化完成之前就使用的问题,因为无法确定类与类之间的初始化顺序
5,了解C++默默编写并调用那些函数
编译器可以暗自为class创建default构造函数,copy构造函数,copy assignment赋值操作符,以及析构函数.
6,若不想使用编译器自动生成的函数,就该明确拒绝
将copy构造函数和赋值操作符声明为private成员函数且不去实现它们.
7,为多态基类声明virtual析构函数
delete一个具有多态性质的基类指针是未定义的行为,这将导致派生类的析构函数无法正常调用.因为为具有多态性质的基类定义virtual析构函数.
8,别让异常逃离析构函数
在析构函数中发生的异常不容许扩散出去,应该捕获异常,并选择终止或吞下该异常.
9,绝不在构造或者析构函数中调用virtual函数
这绝对视一种诡异的行为...
10,令operator=返回一个reference to *this
这是一个实现的协议,为了兼容连锁赋值操作,就像这样:
Wiget& operator=(const Wiget& rhs)
{
//do something
return *this;
}
11,在operator=中处理”自我赋值”
潜在的自我赋值必然存在,而且未必能立马识别出来.既然实现了operator=就必然要考虑到自我赋值的情况,参见10点
Wiget& operator=(const Wiget& rhs)
{
if (this == &rhs)
return *this;
//do something
return *this;
}
12,复制对象时视勿忘其每一个成分
新增成员后忘记对拷贝构造函数和复制操作函数进行同步修改;
如果基类实现了复制操作函数,在派生类的复制操作函数应显示调用,以保证基类也被正确的复制.
13,以对象管理资源
A）为了防止内存泄露，请使用RAII对象，在构造函数中获取资源，在析构函数中释放资源，用栈中的局部变量管理堆内存。
B）std::auto_ptr只保存一份指针对象，赋值语句的右值将被置为NULL。而std::tr1::shared_ptr则是引用计数型智能指针，但是只能针对单个对象使用，对象数组应使用shared_array。
std::auto_ptr<Wiget> ap(new Wiget);
std::tr1::shared_ptr<Wiget> sp(new Wiget);
14,在资源管理类中小心copying行为
用来管理堆内存的RAII对象发生了复制行为会怎样？如果RAII对象是浅拷贝，这将简单的复制指针，当RAII对象析构的时候，指针指向的内存将被重复释放，如果RAII对象视深拷贝，这复制一份指针指向的内存，虽然正常但不是我们所要的。避免发生复制行为：
A)显试定义拷贝构造函数和赋值操作符函数，但不实现它，禁止复制行为。
B)使用复制增加引用计数的方式来确定何时内存应该被释放
C)不仅可以管理内存，还可以管理其它资源，如下：
class Lock {
public:
explicit Lock(Mutex* pm):mutextPtr(pm, unlock)
{
lock(mutexPtr.get());
}
private:
std::tr1::shared_ptr<Mutext> mutexPtr;
};
调用：
Mutex m;
{
Lock ml(&m); //进入临界区
..... //再也不用担心ml被复制了
}
局部变量被自动释放。shared_ptr自动调用删除器unlock，解锁临界区。
15，在资源管理类中提供对原始资源的访问
提供get方法，或者重载operator->,operator*,不提倡operator T() const,可能带来隐式转换。
16，成对使用new和delete要采用相同的形式
new对应delete，new[]对应delete[]。警惕typedef蒙蔽了你的双眼。如:
typedef int vec[100];
int *p = new vec;
delete vec; //error
17，以独立的语句将newd对象置于shared_ptr之中
process(std::tr1::shared_ptr<Wiget> pW(new Wiget), f1());
上述函数参数做了3件事：new Wiget, f1(), 构造shared_ptr;顺序不能确定，假如f1()异常将导致new Wiget丢失。应该将智能指针构造独立出来：
std::tr1:;shared_ptr<Wiget> pW(new Wiget);
process(pW, f1());
18,让接口容易被正确使用，不易被误用
A）重载operator*时返回const 对象，禁止被当做左值使用。
B）确保接口能被正确的调用
C）谁使用谁负责的思想在跨DLL时行不通，new/delete成对使用将导致运行时错误，应使用shared_ptr提供的删除器，将内存管理职责收回。
19，设计Class犹如设计Type
A）新type的对象应该如何被创建和销毁？new/delete，new[]/delete[]
B）对象初始化和对象赋值又怎样的差别？不要混淆什么是初始化，什么是赋值
C）新type的对象被pass by value意味着什么？对象拷贝
D）什么是新type的合法值？约束成员的属性
E）新的type需要配合某个继承图系吗？注意多态应该实现virtual析构函数
F）新type需要什么样的转换？explicit 构造函数不容许隐式转换，但是数值类型例外
G）什么样的操作符和函数对新type而言是合理的？约束行为属性
H）什么样的标准函数应该驳回？约束class的默认行为
I）谁该取用新type的成员？类的封装和抽象
J）什么视新type的“未声明接口”？资源管理，效率，安全性定义
K）新的type有多么一般化？模板化，特化
L）你真的需要一个新的type？一个新的type以上都是要考虑的
20，宁以pass-by-reference-to-const替换pass-by-value
A）前者更加高效，避免了赋值类的开销，也避免了类被切割问题；
B）除了自定义类（也有例外），内置类型和STL迭代器、函数对象传值更加妥当。
21，返回对象时，别妄想返回其reference
局部变量和临时变量不能作为指针或者引用返回，其内存随作用域结束而释放。
22，将成员变量声明为private
所谓越是看不见牵扯越少，提供更好的封装性，数据一致性，弹性。
23，宁以non-member,non-friend替换member函数
至少没有说服我...
24，若所有参数皆需类型转换，请为此采用non-member函数
佐证第23条，operator*实现两个不同版本哪个好？
版本1：
class Rational {
public:
const Rational operator*(const rational& rhs) const;
};
版本2：
class Rational {};
const Rational operator*(const Rational& lhs, const Rational& rhs)
{
return Rational(lhs..., rhs...); 
}
参考代码：
#include <stdio.h>

class Rational 
{
public:
  Rational();
  Rational(int ca = 0, int cb= 0)
    : a(ca), b(cb)
  {}
  void print()
  {
    printf("%d, %d\n", a, b);
  }
public:
  int a;
  int b;
};

const Rational operator*(const Rational& lhs, const Rational& rhs)
{
  return Rational(lhs.a + rhs.a, lhs.b + rhs.b);
}

int main(int argc, char* argv[])
{
  Rational r1(1, 2);
  Rational r2(3, 4);
  Rational r3 = r1 * r2;
  Rational r4 = r1 * 2;
  Rational r5 = 2 * r1;
  r1.print();
  r2.print();
  r3.print();
  r4.print();
  r5.print();
  return 0;
}
25，考虑写一个不抛出异常的swap函数
正确的调用std::swap：
using std::swap;
swap(obj1, obj2);
26，尽可能的延后变量定义式的出现时间
为了改善程序效率，遵循使用时再定义的原则。
27，尽少做转型动作
const_cast将对象的常量性移除
static_cast强迫隐式转换
dynamic_cast执行安全向下转型，不建议使用通常使用virtual函数实现调用
reinterpret_cast执行低级转型
28，避免返回handles指向对象内部成分
将成员定义为private，由提供方法get出来返回成员的引用、指针或迭代器，这是自相矛盾的。
29，为“异常安全”而努力是值得的
异常安全函数会不泄露任何资源，不容许数据被破坏。
void PrettyMenu::changeBackgroud(std::istream& imgSrc)
{
lock(&mutex);
delete bgImage;
bgImage = new Image(imgSrc); //异常发生点
unlock(&mutex); //永远不会被unlock
}
void PrettyMenu::changeBackgroud(std::istream& imgSrc)
{
Lock ml(&mutex) //参看第14点定义
delete bgImage;
bgImage = new Image(imgSrc); //异常发生点
//函数返回就会unlock
}
30，透过了解inlining的里里外外
inline减少了函数调用的开销，什么时候申明为inline函数应该谨慎。
31，将文件间的编译依存关系降至最低
对于C++类而言，如果它的头文件变了，那么所有这个类的对象所在的文件都要重编，但如果它的实现文件（cpp文件）变了，而头文件没有变（对外的接口不变），那么所有这个类的对象所在的文件都不会因之而重编。因此，避免大量依赖性编译的解决方案就是：在头文件中用class声明外来类，用指针或引用代替变量的声明；在cpp文件中包含外来类的头文件。
32，确定你的public继承塑模出来视is-a关系
33，避免掩盖继承而来的名称
派生类会掩盖所有基类的同名函数，可使用using base::func;在派生类中可见。
34，区分接口继承和实现继承
pure virtual函数只具体指定接口继承
impure virtual函数具体指定接口继承及缺省实现继承
non-virtual函数具体指定接口继承以及强制性实现继承
35，考虑virtual函数以外的其它选择
A）使用non-virtual interface(NVI)手法
B）将virtual函数替换为“函数指针成员变量”
C）以tr1::function成员变量替换virtual函数
D）将一个继承体系内的virtual函数替换为另一个继承体系内的virtual函数
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
36，绝不重新定义继承而来的non-virtual函数
37，绝对不要重新定义继承而来的参数值
39，明智而审慎的使用private继承
40，明智而审慎的时候多重继承
41，了解隐式接口和编译器多态
面向对象编程世界总是以显式接口和运行期多态来解决问题，而模板元编程这相反。
发生在编译期间的template具现化成为编译期多态。
class和template都支持接口和多态。
对class而言接口是显示的，以函数签名为中心，多态则是通过virtual函数发生在运行期。
对template参数而言，接口是隐式的，奠基于有效表达式，多态则是通过template具现化和函数重载解析发生于编译期。
42，了解typename的双重意义
声明template参数时，前缀关键字class和typename是完全一样的。
请使用typename标识嵌套从属类型名称，但不得在基类列或成员初始列内使用。
43，学习处理模板化基类内的名称
模板特化即针对某种类型的进行特殊处理，不再通过通用模板编译代码。
派生类模板调用基类模板的成员函数时应告诉编译期怎样调用，可通过this或using 指明调用基类函数
44，将与参数无关的代码抽离
这些代码将导致template具现化所带来的代码膨胀
45，运用成员函数模板接受所有兼容类型
如何在模板内定义成员函数模板，在定义了泛化构造和赋值操作函数之后，仍应显示定义一般式。
46，需要类型转换时请为模板定义非成员函数
请参看第24点
#include <iostream>

template<typename T>
class Rational;

template<typename T>
const Rational<T> doMultiply(const Rational<T>& , const Rational<T>&);

template<typename T>
class Rational 
{
public:
  Rational<T>(T ca, T cb)
    : a(ca), b(cb)
  {}
  void print()
  {
    std::cout << a << "," << b << std::endl;
  }
  friend const Rational<T> operator*(const Rational<T>& lhs, const Rational<T>& rhs)
  {
    return doMultiply(lhs, rhs);
  }
public:
  T a;
  T b;
};

template<typename T>
const Rational<T> doMultiply(const Rational<T>& lhs, const Rational<T>& rhs)
{
  return Rational<T>(lhs.a + lhs.a, lhs.b + rhs.b);
}

int main(int argc, char* argv[])
{
  Rational<int> r1(1, 2);
  Rational<int> r2(3, 4);
  Rational<int> r3 = r1 * r2;
  Rational<double> r4(10.0, 20.0);
  Rational<double> r5 = r4 * r4;
  r1.print();
  r2.print();
  r3.print();
  r4.print();
  r5.print();
  return 0;
}
47，请使用traits classes变现类型信息
48，认识template模板元编程
#include <stdio.h>

template<unsigned n>
struct ftor 
{
  enum{nValue = n * ftor<n-1>::nValue};
};

template<>
struct ftor<0>
{
  enum{nValue = 1};
};

int main(int argc, char* argv[])
{
  printf("%d\n", ftor<5>::nValue);
  return 0;
}
49，了解new-handler的行为
std::set_new_handler
std::get_new_handler
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
50，定制new和delete
A）为了效能
B）为了收集使用上的统计数据
C）为了检测运用错误
D）为了收集动态分配内存之使用统计信息
E）为了增加分配和归还速度
F）为了降低缺省内存管理器带来的空间额外开销
G）为了弥补缺省分配器中的非最佳位对齐
H）为了将对象成簇集中
51，编写new和delete时需固守常规
52，写了placement new也要写placement delete
定制版的new/delete要对应，同时主要不要掩盖正常版本
53，不要忽略编译器警告
严肃对待编译期发出来的抱怨，也不能过分依赖编译，每个编译器都有不同。
54，让自己熟悉包括TR1在内的标准程序库
55,让自己熟悉boost



