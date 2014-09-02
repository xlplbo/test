#include <string.h>
#include <time.h>
#include <stdlib.h>

//cdkey
#define MAX_MASK_LEN		5
#define MAX_PASS_LEN		(2 * MAX_MASK_LEN)
#define CK_ISNUM(c)			(c >= '0' && c <= '9')
#define CK_ISCHAR(c)		(c >= 'A' && c <= 'Z')

const char* CK_MASK_TABLE = "3ZOEA5UI4FP2BQGC7SVHD9W1KRM0TX8LJNY6";

inline void cdkeyGenMask(char* szMask)
{
	int nSize = strlen(CK_MASK_TABLE);
	srand((unsigned)time(NULL));
	int nRand = rand() % nSize;
	for (int i = 0; i < MAX_MASK_LEN; i++)
	{
		szMask[i] = CK_MASK_TABLE[(nRand + i * 3) % nSize];
	}
	szMask[MAX_MASK_LEN] = '\0';
}

inline void cdkeySwapChars(char* sz)
{
	char c;
#define CDKEY_SWAP(n1, n2)	c = sz[n1]; sz[n1] = sz[n2]; sz[n2] = c

	CDKEY_SWAP(0, 9);
	CDKEY_SWAP(1, 6);
	CDKEY_SWAP(3, 8);
}

inline int cdKeyLocateIndex(char c)
{
	for (int i = 0; i < strlen(CK_MASK_TABLE); i++)
	{
		if (c == CK_MASK_TABLE[i])
		{
			return i;
		}
	}
	return -1;
}

inline int cdkeyEncrypt(char* szResult, const char* szPass)
{
	if (!szResult || !szPass || strlen(szPass) != MAX_MASK_LEN)
		return 0;

	char szMask[MAX_MASK_LEN + 1] = "";
	cdkeyGenMask(szMask);

	int nMaskIndex = -1;
	int nPassIndex = -1;
	int nSize = strlen(CK_MASK_TABLE);
	for (int i = 0; i < MAX_MASK_LEN; i++)
	{
		nMaskIndex = CK_ISCHAR(szMask[i]) || CK_ISNUM(szMask[i]) ? cdKeyLocateIndex(szMask[i]) : -1;
		nPassIndex = CK_ISCHAR(szPass[i]) || CK_ISNUM(szPass[i]) ? cdKeyLocateIndex(szPass[i]) : -1;
		if (-1 == nMaskIndex || -1 == nPassIndex)
			return 0;
		szResult[i] = CK_MASK_TABLE[(nPassIndex + nMaskIndex) % nSize];
	}
	for (int i = MAX_MASK_LEN; i < MAX_PASS_LEN; i++)
	{
		szResult[i] = szMask[i - MAX_MASK_LEN];
	}
	szResult[MAX_PASS_LEN] = '\0';
	cdkeySwapChars(szResult);
	return 1;
}

inline int	cdkeyDecrypt(char* szResult, const char* szEncrypted)
{
	if (!szEncrypted || strlen(szEncrypted) != MAX_PASS_LEN)
		return 0;
	char szPass[MAX_PASS_LEN + 1] = "";
	strncpy_s(szPass, szEncrypted, sizeof(szPass));
	cdkeySwapChars(szPass);

	int nMaskIndex = -1;
	int nPassIndex = -1;
	int nSize = strlen(CK_MASK_TABLE);
	for (int i = 0, j = MAX_MASK_LEN; i < MAX_MASK_LEN; i++, j++)
	{
		nMaskIndex = CK_ISCHAR(szPass[j]) || CK_ISNUM(szPass[j]) ? cdKeyLocateIndex(szPass[j]) : -1;
		nPassIndex = CK_ISCHAR(szPass[i]) || CK_ISNUM(szPass[i]) ? cdKeyLocateIndex(szPass[i]) : -1;
		if (-1 == nMaskIndex || -1 == nPassIndex)
			return 0;
		szResult[i] = CK_MASK_TABLE[nPassIndex >= nMaskIndex ? nPassIndex - nMaskIndex : nSize + nPassIndex - nMaskIndex];
	}
	szResult[MAX_MASK_LEN] = '\0';
	return 1;
}
