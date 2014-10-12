#include <stdio.h>
#include <sys/stat.h>
#include <errno.h>
#include <fcntl.h>

int main(int argc, char* argv[])
{
  int fd;
  int nRead;
  char szBuff[128];
  const char* szPath = "/tmp/fifo";

  fd = open(szPath, O_RDONLY, 0);
  if (-1 == fd)
    {
      printf("open fifo error\n");
      goto exit;
    }

  while(1)
    {
      if((nRead = read(fd, szBuff, sizeof(szBuff))) == -1)
        {
          if (errno == EAGAIN)
            printf("no data\n");
        }
      if (szBuff[0] == 'Q')
        break;
      szBuff[nRead] = '\0';
      printf("data:%s\n", szBuff);
      sleep(1);
    }
exit:
  return 0;
}
