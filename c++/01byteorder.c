#include <stdio.h>
#include <arpa/inet.h>

int main(int argc, char* argv[])
{

  unsigned int n = 0x12345678;
  unsigned char* p = (unsigned char*)&n;
  printf("%0x %0x %0x %0x\n", p[0], p[1], p[2], p[3]);
  unsigned int m = htonl(n);
  p = (unsigned char*)&m;
  printf("%0x %0x %0x %0x\n", p[0], p[1], p[2], p[3]);

  unsigned long addr = inet_addr("192.168.77.100");
  printf("addr=%lu\n", addr);

  struct in_addr ipaddr;
  ipaddr.s_addr = addr;
  printf("%s\n", inet_ntoa(ipaddr));
  return 0;
}
