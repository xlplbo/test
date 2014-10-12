#include <stdio.h>

template<unsigned n>
struct ftor 
{
  enum{nValue = n * ftor<n-1>::nValue};
};

template<>
struct ftor<0>
{
  enum{nValue = 1};
};

int main(int argc, char* argv[])
{
  printf("%d\n", ftor<5>::nValue);
  return 0;
}
