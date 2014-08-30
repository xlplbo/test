#include <iostream>
#include <stdlib.h>
#include <string>
#include "1.h"

using namespace std;

int main()
{
    char* str = "asflsdkjqwpoeirp";
    cout << IsUniqueString(str, strlen(str)) << endl;

    char str1[100] = "asdfghjkl";
    ReverseString(str1, strlen(str1));
    cout << str1 << endl;

    string a = "asdfgh";
    string b = "hgasdf";
    cout << IsPermutation(a, b) << endl;

    return 0;
}
