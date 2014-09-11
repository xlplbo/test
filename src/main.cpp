#include <iostream>
#include <stdlib.h>
#include <string>
#include "1.h"
#include "cdkey.h"

using namespace std;

int main()
{
    char* str = "asflsdkjqwpoeirp";
    cout << IsUniqueString(str, strlen(str)) << endl;

    char str1[100] = "asdfghjkl";
    ReverseString(str1, strlen(str1));
    cout << str1 << endl;

    string a = "asdfgh";
    string b = "fghasd";
    cout << IsPermutation(a, b) << endl;

	cout << IsRatation(a, b) << endl;

	char result[11] = "";
	char* passwd = "QWERT";
	cdkeyEncrypt(result, passwd);
	cout << result << endl;
	char result1[6] = "";
	cdkeyDecrypt(result1, result);
	cout << result1 << endl;

	for (int i = 1; i <= 30; i++)
	{
		unsigned long long nValue = 1;
		for (int j = 1; j <= i; j++)
		{
			nValue *= j;
		}
		cout << i << " " << nValue << " " << CountZero(i) << " " << CountZero2(i)  << endl;
	}

	system("PAUSE");
    return 0;
}
