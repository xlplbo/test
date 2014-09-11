#include <algorithm>

//1.1
//�����ַ����Ƿ����ظ��ַ�
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
//��ת�ַ���
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
//�Ƚ������ַ����Ƿ�Ϊ��λ��
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
//�Ƿ�Ϊ��ת�ַ�
bool IsRatation(std::string a, std::string b)
{
	if (a.length() != b.length())
		return false;
	std::string aa = a + a;
	if (aa.find(b) != std::string::npos)
		return true;
	return false;
}


int CountZero(int n)
{
	unsigned long long nValue = 1;
	for (int i = 2; i <= n; i++)
	{
		nValue *= i;
	}
	int nCount = 0;
	while (0 == nValue % 10)
	{
		nCount++;
		nValue /= 10;
	}
	return nCount;
}

int CountZero2(int n)
{
	int count = 0;
	if (n < 0)
		return -1;
	for (int i = 5; n / i>0; i *= 5)
		count += n / i;
	return count;
}