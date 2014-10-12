#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 20
typedef double (*f)(int, int, char); //function point
typedef int vecInt[MAX_SIZE]; //vector int
typedef int (*vec)[MAX_SIZE];

double calc(int a, int b, char op)
{
  switch(op)
    {
    case '+':
      return a + b;
    case '-':
      return a - b;
    case '*':
      return a * b;
    case '/':
      return a / b;
    }
}

int main(int argc, char* argv[])
{
  f func = calc;
  printf("%lf\n",func(2,3,'-'));
  vecInt a = {
    1, 2, 3, 4, 5, 
    1, 2, 3, 4, 5,
    1, 2, 3, 4, 5,
    1, 2, 3, 4, 5,
  };
  for (int i = 0; i < MAX_SIZE; i ++)
    {
      printf("a[%d] = %d\n", i, a[i]);
    }
  vec b;
  int c[2][MAX_SIZE] = {0};
  b = c;
  b[0][0] = 1;
  printf("%d\n", b[0][0]);
  return 0;
}
