#include "net.h"

int main(int argc, char* argv[])
{
    int listenfd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, IPPROTO_TCP);
    if (listenfd < 0)
        ERR_EXIT("socket");

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(8989);
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(listenfd, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) < 0)
        ERR_EXIT("bind");

    int on;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)) < 0)
        ERR_EXIT("setsockopt");

    if (listen(listenfd, SOMAXCONN) < 0)
        ERR_EXIT("listen");
	
	signal(SIGCHLD, handler_child);
    
	fd_set rfds;
	FD_ZERO(&rfds);
	FD_SET(listenfd, &rfds);
	while(1)
	{	
		int retval = select(listenfd+1, &rfds, NULL, NULL, NULL);
		if (retval < 0)
		{
			if (errno == EINTR)
				continue;	
			ERR_EXIT("select");
		}
		if (FD_ISSET(listenfd, &rfds))
		{
			struct sockaddr_in peeraddr;
			socklen_t peerlen = sizeof(peeraddr);
			int conn = accept(listenfd, (struct sockaddr*)&peeraddr, &peerlen);
			if (conn < 0)
				ERR_EXIT("accept");
			
			pid_t pid = fork();
			if (pid < 0)
				ERR_EXIT("fork");
			else if (pid > 0)
			{
				printf("child pid %d create\n", pid);
				continue;
			}
			else
			{
				printf("ip=%s:%d\n", inet_ntoa(peeraddr.sin_addr), ntohs(peeraddr.sin_port));
				fd_read_write(conn);
				shutdown(conn, SHUT_RDWR);
				break;
			}
		}
	}
	close(listenfd);
    return 0;
}
