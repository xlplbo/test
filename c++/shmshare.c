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

int main(int argc, char* argv[])
{
	int shmid = shmget(IPC_PRIVATE, 1024, IPC_CREAT | 0666);
	if (shmid < 0)
	{
		perror("shmget");
		exit(EXIT_FAILURE);
	}
	printf("create shared memory OK, size = 1024, shmid = %d\n", shmid);

	char* buff = (char*)shmat(shmid, NULL, 0);
	if ((int)buff == -1)
	{
		perror("shmat");
		exit(EXIT_FAILURE);
	}
	memset(buff, 0, 1024);
	char temp[1024] = "";
	scanf("%s", temp);
	strncpy(buff, temp, 1024);

	shmctl(shmid, IPC_RMID, NULL);
	return 0;
}
