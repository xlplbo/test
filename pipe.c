#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, int* argv[])
{
  int n;
  int fd[2];
  pid_t pid;
  char line[128];
  
  if (pipe(fd) < 0)
    {
      printf("pipe error\n");
      goto exit;
    }

  if ((pid = fork()) < 0)
    {
      printf("fork error\n");
      goto exit;
    }
  else if (pid == 0)
    {
      close(fd[1]);
      n = read(fd[0], line, 128);
      printf("Parent'Pid print something to stdout:\n");
      write(1, line, n);
    }
  else
    {
      close(fd[0]);
      char szBuff[128] = "";
      snprintf(szBuff, sizeof(szBuff), "i am %d, Hello Parent!\n", getpid());
      write(fd[1], szBuff, strlen(szBuff));
    }

  if (waitpid(pid, NULL, 0) != pid)
    {
      printf("waitpid: i am %d \n", getpid());
      // _exit(0);
    }
  printf("i am %d \n", getpid());
exit:
  return 0;
}
