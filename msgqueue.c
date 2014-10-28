#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>   
#include <sys/ipc.h>   
#include <sys/msg.h>   
#include <errno.h>   
 
#define MSGKEY 1234   
   
int main(int agrc, char* agrv[])  
{  
  struct msgstru 
  {
	long msgtype;
	char msgtext[2048];
  } msgs;  
  int msg_type;  
  char str[256];  
  int ret_value;  
   
  int msqid=msgget(MSGKEY,IPC_EXCL);  /*检查消息队列是否存在*/  
  if(msqid < 0)
  {  
    msqid = msgget(MSGKEY,IPC_CREAT|0666);/*创建消息队列*/  
    if(msqid <0)
	{  
		perror("msgget");  
		exit(EXIT_FAILURE);  
    }  
  }   

  pid_t pid = fork();
  if (pid < 0)
	  exit(EXIT_FAILURE);
  else if (pid > 0)
  {
	while(1)
	{  
		msqid = msgget(MSGKEY,IPC_EXCL );/*检查消息队列是否存在 */  
		if (msqid < 0)
		{  
			perror("msgget");  
			break;
		}
		/*接收消息队列*/  
		ret_value = msgrcv(msqid,&msgs,sizeof(struct msgstru),0,0);  
		printf("text=[%s] pid=[%d]\n",msgs.msgtext,getpid());  
	}  
  }
  else
  {
	while (1)
	{  
		printf("input message type(end:0):");  
		scanf("%d",&msg_type);  
		if (msg_type == 0)  
			break;  
		printf("input message to be sent:");  
		scanf ("%s",str);  
		msgs.msgtype = msg_type;  
		strcpy(msgs.msgtext, str);  
		/* 发送消息队列 */  
		ret_value = msgsnd(msqid,&msgs,sizeof(struct msgstru),IPC_NOWAIT);  
		if ( ret_value < 0 ) 
		{  
			perror("msgsend");  
			exit(EXIT_FAILURE);  
		} 
	}
  }  
  msgctl(msqid,IPC_RMID,0); //删除消息队列   
}
