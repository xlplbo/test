#include <iostream>
#include <memory>
#include <map>
int main(int argc, char* argv[])
{
	// auto�����ƶ�
	std::map<int, int> mapInt;
	mapInt.insert(std::pair<int, int>(1, 2));
	mapInt.insert(std::pair<int, int>(2, 4));

	// foreach
	for (auto& it : mapInt)
	{
		std::cout << it.first << " " << it.second << std::endl;
	}

	// NULL��ʽת��Ϊint, nullptr��ʽת��Ϊbool
	char* p = NULL;
	char* q = nullptr;
	bool  b = nullptr;

	// override��д�����麯����final�����಻����д�����麯��
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
		//virtual void g(int) { std::cout << "A::g" << std::endl; } // error C3248: ��main::A::g��:  ����Ϊ��final���ĺ����޷�����main::B::g����д
		virtual void g(float) { std::cout << "A::g" << std::endl; } // ����
	};

	// ǿ����ö��,���ٵ��������������ͻ
	enum class eType {
		eT_NONE,
		eT_RED,
		eT_GREEN,
		eT_BLUE,
	};
	//int eT_NONE = eType::eT_NONE; // error C2440: ����ʼ����: �޷��ӡ�main::eType��ת��Ϊ��int��

	// ����ָ��
	std::unique_ptr<int> p1(new int(42));
	std::unique_ptr<int> p2 = std::move(p1); // �ƽ�uniqueָ��

	auto sp = std::make_shared<int>(42);
	std::weak_ptr<int> wp = sp;

	{
		auto sp = wp.lock(); // ����shared_ptr
		std::cout << *sp << std::endl;
	}

	sp.reset();

	if (wp.expired())
		std::cout << "expired" << std::endl;

	// Lambdas��������
	system("PASUE");
	return 0;
}