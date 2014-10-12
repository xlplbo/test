#include <algorithm>
#include <cstdlib>

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

int MyRand(int low, int high)
{
	return low + rand() % (high - low + 1);
}

int* shuffle(int* cards, int n)
{
	if (n <= 0)
		return cards;

	shuffle(cards, n - 1);
	int rand = MyRand(0, n);

	int temp = cards[rand];
	cards[rand] = cards[n];
	cards[n] = temp;

	return cards;
}

void shuffle2(int* cards, int n)
{
	// ���i-1��������һ������i����
	for (int i = 0; i < n; i++)
	{
		int rand = MyRand(0, i);
		int temp = cards[rand];
		cards[rand] = cards[i];
		cards[i] = temp;
	}
}

void* aligned_malloc(size_t size, size_t alignd_byte)
{
	//offset��ַƫ����(byte)
	//alignd_byte�����ֽڵ�Ԥ����ռ�
	//sizeof(void *)������ʵָ���Ԥ����ռ�
	size_t offset = sizeof(void *) + alignd_byte - 1;

	//Ԥ���������ڴ��
	//qָ������ڴ���׵�ַ
	void* q = malloc(size + offset);
	if (!q)
		return NULL;
	//printf("q = 0x%p\n", q);

	//�������ڴ��
	//��������qָ�붼���ƫ�ƣ���& ~(alignd_byte - 1)��ַ����
	void* p = (void *)(((size_t)(q)+offset) & ~(alignd_byte - 1));
	//Ϊ�����free����������qָ�뵽p-1��λ��
	//p[-1] = q;ֱ������������void *��Сδ֪�޷�Ѱַ
	*(((void **)p) - 1) = q;

	//���ض�����ָ��
	return p;
}

void aligned_free(void* p)
{
	//����ԭ�ڴ����׵�ַ
	void* q = ((void **)p)[-1];
	free(q);
}