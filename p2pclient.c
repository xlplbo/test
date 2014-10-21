#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

#define ERR_EXIT(m) \
  do                                            \
    {                                           \
      perror(m);                                \
      exit(EXIT_FAILURE);                       \
    } while(0)

void handler(int sig)
{
  printf("signal exit %d\n", sig);
  exit(EXIT_SUCCESS);
}

int main(int argc, char* argv[])
{
  int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (sock < 0)
    ERR_EXIT("socket");
  
  struct sockaddr_in serveraddr;
  memset(&serveraddr, 0, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_port = htons(8989);
  //serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_addr.s_addr = inet_addr("127.0.0.1");

  if (connect(sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) < 0)
    ERR_EXIT("connect");
  
  pid_t pid = fork();
  if (pid < 0)
    ERR_EXIT("fork");
  else if (pid == 0)
    {
      signal(SIGUSR1, handler);
      char sendbuf[1024] = {0};
      while(fgets(sendbuf, sizeof(sendbuf), stdin) != NULL)
        {
          write(sock, sendbuf, strlen(sendbuf));
          memset(sendbuf, 0, sizeof(sendbuf));
        }
    }
  else
    {
      char recvbuf[1024];
      while(1)
        {
          memset(recvbuf, 0, sizeof(recvbuf));
          int ret = read(sock, recvbuf, sizeof(recvbuf));
          if (ret == 0)
            {
              printf("svr close\n");
              break;
            }
          else if (ret == -1)
            ERR_EXIT("read = -1");
          else
            fputs(recvbuf, stdout);
        }
      kill(pid, SIGUSR1);
      close(sock);
    }
  
  return 0;
}
