#include <iostream>
#include <stdlib.h>
#include <string>
#include "1.h"
#include "cdkey.h"

using namespace std;

int main()
{
	//重复字符检查
    char* str = "asflsdkjqwpoeirp";
    cout << IsUniqueString(str, strlen(str)) << endl;

	//反转字符串
    char str1[100] = "asdfghjkl";
    ReverseString(str1, strlen(str1));
    cout << str1 << endl;

	//变位词
    string a = "asdfgh";
    string b = "fghasd";
    cout << IsPermutation(a, b) << endl;

	//旋转字符串
	cout << IsRatation(a, b) << endl;

	//简单加密算法，每次加密的结果都不一样
	char result[11] = "";
	char* passwd = "QWERT";
	cdkeyEncrypt(result, passwd);
	cout << result << endl;
	char result1[6] = "";
	cdkeyDecrypt(result1, result);
	cout << result1 << endl;

	//求尾随零的个数
	for (int i = 1; i <= 30; i++)
	{
		unsigned long long nValue = 1;
		for (int j = 1; j <= i; j++)
		{
			nValue *= j;
		}
		cout << i << " " << nValue << " " << CountZero(i) << " " << CountZero2(i)  << endl;
	}

	//完美洗牌算法
	for (int k = 1; k <= 10; k++)
	{
		int cards[52] = { 
			1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
			14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
			25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
			36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
			47, 48, 49, 50, 51, 52,
		};	
		cout << endl;
		//shuffle(cards, 52);
		shuffle2(cards, 52);
		for (int i = 1; i <= 52; i++)
		{
			cout << cards[i - 1] << " ";
			if (i % 13 == 0)
				cout << endl;
		}
	}
	cout << endl;
	system("PAUSE");
    return 0;
}
