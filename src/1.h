#include <algorithm>

//1.1
//给定字符串是否有重复字符
bool IsUniqueString(const char * des, int nSize)
{
    bool char_set[128] = {false};
    for (int i = 0; i < nSize; i ++)
    {
        if (char_set[des[i]])
            return false;
        char_set[des[i]] = true;
    }
    return true;
}

//1.2
//翻转字符串
void ReverseString(char * des, int nSize)
{
    char tempChar;
    int nCount = nSize / 2;
    for (int i = 0; i < nCount; i ++)
    {
        tempChar = des[i];
        des[i] = des[nSize - 1 - i];
        des[nSize - 1 - i] = tempChar;
    }
}

//1.3
//比较两个字符串是否为变位词
bool IsPermutation(std::string &a, std::string &b)
{
    if (a.length() != b.length())
        return false;

    sort(a.begin(), a.end());
    sort(b.begin(), b.end());

    if (a != b)
        return false;

    return true;
}

//1.8
//是否为旋转字符
bool IsRatation(std::string a, std::string b)
{
	if (a.length() != b.length())
		return false;
	std::string aa = a + a;
	if (aa.find(b) != std::string::npos)
		return true;
	return false;
}
