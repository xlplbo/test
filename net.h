#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>

#define ERR_EXIT(m)            \
    do                         \
    {                          \
      perror(m);               \
      exit(EXIT_FAILURE);      \
    } while(0)

#define MAX_BUFF_SIZE 1024

ssize_t readn(int fd, void *buf, size_t count)
{
    size_t left = count;
    unsigned int* p = (unsigned int*)buf;

    while(left > 0)
    {
        ssize_t nread = read(fd, p, left);
        if (nread == -1)
			ERR_EXIT("read");
		if (nread == 0)
			return 0;
        p += nread;
        left -= nread;
    }
	return -1;
}

ssize_t writen(int fd, const void *buf, size_t count)
{
    size_t left = count;
    unsigned int* p = (unsigned int*)buf;

    while(left > 0)
    {
        ssize_t nwrite = write(fd, p, left);
        if (nwrite == -1)
			ERR_EXIT("write");
		if (nwrite == 0)
			return 0;
        p += nwrite;
        left -= nwrite;
    }
	return -1;
}

void fd_read_puts(int sockfd)
{
	fd_set rfds;
    FD_ZERO(&rfds);

	char buff[MAX_BUFF_SIZE] = "";
	while (1)
	{
		FD_SET(sockfd, &rfds);
	    int retval = select(sockfd+1, &rfds, NULL, NULL, NULL);
		if (retval == -1)
			ERR_EXIT("select()");
		if (retval == 0)
			continue;
		if (FD_ISSET(sockfd, &rfds))
		{
			memset(buff, 0, sizeof(buff));
			if (0 == readn(sockfd, buff, sizeof(buff)))
				break;
			fputs(buff, stdout);
		}
	}
}

void fd_gets_write(int sockfd)
{
	fd_set rfds;
    FD_ZERO(&rfds);
	int filefd = fileno(stdin);

	char buff[MAX_BUFF_SIZE] = "";
	while (1)
	{
		FD_SET(filefd, &rfds);
	    int retval = select(filefd+1, &rfds, NULL, NULL, NULL);
		if (retval == -1)
			ERR_EXIT("select()");
		if (retval == 0)
			continue;
		if (FD_ISSET(filefd, &rfds))
		{
			memset(buff, 0, sizeof(buff));
			fgets(buff, sizeof(buff), stdin);
			if (0 == writen(sockfd, buff, sizeof(buff)))
				break;
		}
	}
}

void fd_read_write(int conn)
{
	fd_set rfds;
    FD_ZERO(&rfds);

	char buff[MAX_BUFF_SIZE] = "";
	while (1)
	{
		FD_SET(conn, &rfds);
	    int retval = select(conn+1, &rfds, NULL, NULL, NULL);
		if (retval == -1)
			ERR_EXIT("select()");
		if (retval == 0)
			continue;
		if (FD_ISSET(conn, &rfds))
		{
			memset(buff, 0, sizeof(buff));
			if (0 == readn(conn, buff, sizeof(buff)))
				break;
			fputs(buff, stdout);
			if (0 == writen(conn, buff, sizeof(buff)))
				break;
		}
	}
}

void handler_child(int sig)
{
	pid_t pid = 0;
	while((pid = waitpid(-1, NULL, 0)) > 0)
		printf("waitpid %d exit, sig %d\n", pid, sig);
}
