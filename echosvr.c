#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
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
    int listenfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (listenfd < 0)
        ERR_EXIT("socket");

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(8989);
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    // serveraddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    if (bind(listenfd, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) < 0)
        ERR_EXIT("bind");

    int on;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)) < 0)
        ERR_EXIT("setsockopt");

    if (listen(listenfd, SOMAXCONN) < 0)
        ERR_EXIT("listen");

    struct sockaddr_in peeraddr;
    socklen_t peerlen = sizeof(peeraddr);
    int conn;
    pid_t pid;
    while(1)
    {
        conn = accept(listenfd, (struct sockaddr*)&peeraddr, &peerlen);
        if (conn < 0)
            ERR_EXIT("accept");

        printf("ip=%s:%d\n", inet_ntoa(peeraddr.sin_addr), ntohs(peeraddr.sin_port));
        pid = fork();
        if (pid < 0)
            ERR_EXIT("fork");
        else if (pid == 0)
        {
            char recvbuf[1024];

            while(1)
            {
                memset(recvbuf, 0, sizeof(recvbuf));
                int ret = readn(conn, recvbuf, sizeof(recvbuf));
                if (ret == 0)
                {
                    printf("client close\n");
                    break;
                }
                if (ret == -1)
                    ERR_EXIT("read = -1");
                fputs(recvbuf, stdout);
                writen(conn, recvbuf, ret);
            }
        }
        close(conn);
    }
    close(listenfd);
    return 0;
}
