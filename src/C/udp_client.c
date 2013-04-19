/*  UDP  client  in  the  internet  domain  */ 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <arpa/inet.h> 
#include <netdb.h> 
#include <stdio.h> 
#include <stdlib.h> 

#include <arpa/inet.h>  
#include <assert.h>  
#include <errno.h>  
#include <signal.h>  
#include <string.h>  
#include <sys/wait.h>  
#include <netdb.h>  
#include <unistd.h>  

void error(char *msg) 
{ 
    perror(msg); 
    exit(0); 
} 


int main(int argc, char *argv[]) 
{
	int socketFileDescriptor, length, n, count, numberOfPackets; 
	struct sockaddr_in server; 
	struct hostent *hp; 
	char buffer[256]; 

	if (argc != 4) { 
		printf("Usage: server, port, number of packages\n"); 
        exit(1); 
	} 
	
	numberOfPackets = atoi(argv[3]);
	
	socketFileDescriptor= socket(AF_INET, SOCK_DGRAM, 0); 
	if (socketFileDescriptor < 0) 
		error("socket"); 
	
	server.sin_family = AF_INET; 
	hp = gethostbyname(argv[1]); 
	if (hp==0) error("Unknown host"); 
	
	bcopy((char *)hp->h_addr,(char *)&server.sin_addr, hp->h_length);
	
	server.sin_port = htons(atoi(argv[2])); //
	length = sizeof(struct sockaddr_in); 
	
	for(count = 1; count <= numberOfPackets; count ++)
	{
		sprintf(buffer, "this is packet number %d", count);
		n = sendto(socketFileDescriptor, buffer , strlen(buffer),0,&server,length); 
	
		if (n < 0)
			error("sending to server");
	}	
	
	return 0;
	 
} 
