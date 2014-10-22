#include <algorithm>
#include <cstdlib>
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
	// 随机i-1个的任意一个数与i交换
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
	//offset地址偏移量(byte)
	//alignd_byte对齐字节的预分配空间
	//sizeof(void *)保存真实指针的预分配空间
	size_t offset = sizeof(void *) + alignd_byte - 1;
	//预分配更大的内存块
	//q指向这块内存的首地址
	void* q = malloc(size + offset);
	if (!q)
		return NULL;
	//printf("q = 0x%p\n", q);
	//对齐后的内存块
	//不管怎样q指针都向后偏移，再& ~(alignd_byte - 1)地址对齐
	void* p = (void *)(((size_t)(q)+offset) & ~(alignd_byte - 1));
	//为了配合free函数，保存q指针到p-1的位置
	//p[-1] = q;直接这样做不行void *大小未知无法寻址
	*(((void **)p) - 1) = q;
	//返回对齐后的指针
	return p;
}
void aligned_free(void* p)
{
	//计算原内存块的首地址
	void* q = ((void **)p)[-1];
	free(q);
}
