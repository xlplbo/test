/*定义函数返回string数组引用*/
#include <iostream>
#include <string>

std::string str[2] = {
	"test",
	"hello",
};

/*普通式*/
std::string (&func(std::string (&str)[2]))[2]
{
	str[0] = "common";
	return str;
}

/*typedef别名式*/
typedef std::string STR2[2];
STR2& func1(std::string (&str)[2])
{
	str[0] = "typedef";
	return str;
}

/* 尾置返回类型
 * use c++11 
 */
auto func2(std::string (&str)[2]) -> std::string (&)[2]
{
	str[0] = "auto";
	return str;
}

/* 类型推到式
 * use c++11
 */
decltype(str)& func3(std::string (&str)[2])
{
	str[0] = "decltype";
	return str;
}

int main()
{
	func(str);
	std::cout << str[0] << std::endl;
	std::cout << str[1] << std::endl;
	func1(str);
	std::cout << str[0] << std::endl;
	std::cout << str[1] << std::endl;
	func2(str);
	std::cout << str[0] << std::endl;
	std::cout << str[1] << std::endl;
	func3(str);
	std::cout << str[0] << std::endl;
	std::cout << str[1] << std::endl;
	return 0;
}
