#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include "1.h"
#include "cdkey.h"
//#include "SmartPointer.h"

using namespace std;

void main()
{
    //�ظ��ַ����
    char* str = "asflsdkjqwpoeirp";
    cout << IsUniqueString(str, strlen(str)) << endl;

	//��ת�ַ���
    char str1[100] = "asdfghjkl";
    ReverseString(str1, strlen(str1));
    cout << str1 << endl;

	//��λ��
    string a = "asdfgh";
    string b = "fghasd";
    cout << IsPermutation(a, b) << endl;

	//��ת�ַ���
	cout << IsRatation(a, b) << endl;

	//�򵥼����㷨��ÿ�μ��ܵĽ������һ��
	char result[11] = "";
	char* passwd = "QWERT";
	cdkeyEncrypt(result, passwd);
	cout << result << endl;
	char result1[6] = "";
	cdkeyDecrypt(result1, result);
	cout << result1 << endl;

	//��β����ĸ���
	for (int i = 1; i <= 30; i++)
	{
		unsigned long long nValue = 1;
		for (int j = 1; j <= i; j++)
		{
			nValue *= j;
		}
		cout << i << " " << nValue << " " << CountZero(i) << " " << CountZero2(i)  << endl;
	}

	//����ϴ���㷨
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

	//�����ڴ����
	int size = 1234; //��Ҫ������ڴ��С��byte��
	int alignment = 128; //��ַ���루byte��
	void* p = NULL;
	void* q = NULL;

	int nCount = 0;//Ϊ�˲��Բ���δalignment(byte)��������
	while (1)
	{
		nCount++;
		void* p = aligned_malloc(size, alignment); //  ������
		void* q = ((void **)p)[-1]; // δ����������
		if ((size_t)q % alignment != 0)
		{//���malloc����alignment(byte)����
			printf("p = %p, %d\n", p, (size_t)p % alignment);
			printf("q = %p, %d\n", q, (size_t)q % alignment);
			for (size_t i = 1; i <= size / sizeof(int); i++)
			{
				((int *)p)[i - 1] = i;
			}
			for (size_t i = 1; i <= size / sizeof(int); i++)
			{
				printf("%d  ", ((int *)p)[i - 1]);
				if (i % 10 == 0)
					printf("\n");
			}
			printf("\n");
			aligned_free(p);
			break;
		}
		aligned_free(p);
	}
	printf("nCount = %d\n", nCount);
	
	//��������ָ��
	//test_SmartPointer();
	
	system("PAUSE");
    return 0;
}
