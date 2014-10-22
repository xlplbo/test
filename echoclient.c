#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

#define ERR_EXIT(m)                             \
    do                                          \
    {                                           \
      perror(m);                                \
      exit(EXIT_FAILURE);                       \
    } while(0)

ssize_t readn(int fd, void *buf, size_t count)
{
    size_t left = count, npack;
    unsigned int* p = (unsigned int*)buf;

    while(left > 0)
    {
        ssize_t nread = read(fd, p, left);
        if (-1 == nread)
            ERR_EXIT("read");
        else if (0 == nread)
            continue;
        else
        {
            p += nread;
            left -= nread;
        }
    }
}

ssize_t writen(int fd, const void *buf, size_t count)
{
    size_t left = count, npack;
    unsigned int* p = (unsigned int*)buf;

    while(left > 0)
    {
        ssize_t nwrite = write(fd, p, left);
        if (-1 == nwrite)
            ERR_EXIT("read");
        else if (0 == nwrite)
            continue;
        else
        {
            p += nwrite;
            left -= nwrite;
        }
    }
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

    char sendbuff[1024];
    char recvbuff[1024];
    while(fgets(sendbuff, sizeof(sendbuff), stdin) != NULL)
    {
        writen(sock, sendbuff, sizeof(sendbuff));
        readn(sock, recvbuff, sizeof(recvbuff));
        fputs(recvbuff, stdout);
        memset(sendbuff, 0, sizeof(sendbuff));
        memset(recvbuff, 0, sizeof(recvbuff));
    }
    close(sock);
    return 0;
}
