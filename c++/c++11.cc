#include <iostream>
#include <memory>
#include <map>
int main(int argc, char* argv[])
{
	// auto类型推断
	std::map<int, int> mapInt;
	mapInt.insert(std::pair<int, int>(1, 2));
	mapInt.insert(std::pair<int, int>(2, 4));

	// foreach
	for (auto& it : mapInt)
	{
		std::cout << it.first << " " << it.second << std::endl;
	}

	// NULL隐式转换为int, nullptr隐式转换为bool
	char* p = NULL;
	char* q = nullptr;
	bool  b = nullptr;

	// override重写基类虚函数，final派生类不得重写基类虚函数
	class A
	{
	public:
		virtual void f(short) { std::cout << "A::f" << std::endl; }
		virtual void g(int) final { std::cout << "A::g" << std::endl; }
	};

	class B : public A
	{
	public:
		virtual void f(short)  override  { std::cout << "B::f" << std::endl; }
		//virtual void g(int) { std::cout << "A::g" << std::endl; } // error C3248: “main::A::g”:  声明为“final”的函数无法被“main::B::g”重写
		virtual void g(float) { std::cout << "A::g" << std::endl; } // 重载
	};

	// 强类型枚举,不再导致作用域变量冲突
	enum class eType {
		eT_NONE,
		eT_RED,
		eT_GREEN,
		eT_BLUE,
	};
	//int eT_NONE = eType::eT_NONE; // error C2440: “初始化”: 无法从“main::eType”转换为“int”

	// 智能指针
	std::unique_ptr<int> p1(new int(42));
	std::unique_ptr<int> p2 = std::move(p1); // 移交unique指针

	auto sp = std::make_shared<int>(42);
	std::weak_ptr<int> wp = sp;

	{
		auto sp = wp.lock(); // 提升shared_ptr
		std::cout << *sp << std::endl;
	}

	sp.reset();

	if (wp.expired())
		std::cout << "expired" << std::endl;

	// Lambdas匿名函数

	system("PASUE");
	return 0;
}