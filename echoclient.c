#include "net.h"

int main(int argc, char* argv[])
{
	int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0)
        ERR_EXIT("socket");

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(8989);
    serveraddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) < 0)
        ERR_EXIT("connect");
	
	signal(SIGCHLD, handler_child);
	
	pid_t pid = fork();
	if (pid < 0)
		ERR_EXIT("fork");
	else if (pid == 0)
	{
		fd_read_puts(sock);
		close(sock);
	}
	else
	{
		fd_gets_write(sock);
		close(sock);
	}
	return 0;
}
