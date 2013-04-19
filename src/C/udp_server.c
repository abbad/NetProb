#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h> /* for close() for socket */ 
#include <stdlib.h>
 
void error(const char *msg)
{
    perror(msg);
    exit(1);
}
 
int main(int argc, char *argv[])
{
  int socketFileDescriptor, portno; 
  struct sockaddr_in sa; 
  char buffer[1024];
  ssize_t recsize;
  socklen_t fromlen;
  
  if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
  }
   
  socketFileDescriptor = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); //changed PF_INET to AF_INET
  
  if (socketFileDescriptor < 0)
	error("Error creating socket");
  
  memset(&sa, 0, sizeof sa); // set to zero
  
  portno = atoi(argv[1]);
  
  sa.sin_family = AF_INET;
  sa.sin_addr.s_addr = htonl(INADDR_ANY);
  sa.sin_port = htons(portno);
  fromlen = sizeof(sa);
 
  if (-1 == bind(socketFileDescriptor, (struct sockaddr *)&sa, sizeof(sa)))
	error("error bind failed");
  int count = 0;
  while(1) 
  {
    recsize = recvfrom(socketFileDescriptor, (void *)buffer, sizeof(buffer), 0, (struct sockaddr *)&sa, &fromlen);
	count++;
    if (recsize < 0) {
      fprintf(stderr, "%s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }
    printf("recsize: %d\n ", recsize);
	printf("recieved packet number %i\n", count);
    sleep(1);
    printf("datagram: %.*s\n", (int)recsize, buffer);
  }
  
  return 0;
}