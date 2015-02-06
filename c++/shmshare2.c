/*************************************************************************
    > File Name: shmshare.c
    > Author: xlplbo
    > Mail: booxlp@gmail.com
    > Created Time: Tue 28 Oct 2014 07:53:04 AM PDT
 ************************************************************************/

#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include<assert.h>

int main(int argc, char* argv[])
{
	assert(argc == 2);
	int shmid = atoi(argv[1]);
	char* buff = (char*)shmat(shmid, NULL, 0);
	if ((int)buff == -1)
	{
		perror("shmat");
		exit(EXIT_FAILURE);
	}
	while(1)
	{
		if (buff[0])
		{
			printf("buff:%s", buff);
			break;
		}
	}
	shmdt(buff);
	return 0;
}
