#include <sys/fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <signal.h>
#include <sys/ioctl.h>
#include <time.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>

// SERIAL CONFIGURATION
#define BAUDRATE B9600
int fd=-1;
struct termios oldtio,newtio;

// TIMEOUTS
#define USLEEP 100000
#define RETRIES 10
//#define DEBUG 1

// FUNCTION DEFINITION
void port_open(char *device);
int port_read(char *buffer,int len);
int port_write(char *buffer,int len);
void port_close(void);

// ALARM PROTECTION
void alarm_handler(int signum) {
	port_close();
}

// FUNCTION IMPLEMENTATION
int port_read(char *buffer,int len) {
	int retval;

	signal(SIGALRM,alarm_handler);
	alarm(5);
	retval=read(fd,buffer,len);
	if(retval==-1) {
		//~ printf("ERROR: %s (%d)\n",strerror(errno),errno);
		if(errno!=EAGAIN) port_close();
		retval=0;
	}
	alarm(0);
	return retval;
}

int port_write(char *buffer,int len) {
	int retval;

	retval=write(fd,buffer,len);
	return retval;
}

void port_open(char *device) {
	fd=open(device,O_RDWR|O_NOCTTY|O_NONBLOCK);
	if(fd==-1) return;
	tcgetattr(fd,&oldtio);
	bzero(&newtio,sizeof(newtio));
	newtio.c_cflag=CS8|CREAD|CLOCAL;
	newtio.c_iflag=IGNPAR;
	newtio.c_oflag=0;
	newtio.c_lflag=0;
	newtio.c_cc[VTIME]=1;
	newtio.c_cc[VMIN]=1;
	tcflush(fd,TCIOFLUSH);
	cfsetispeed(&newtio,BAUDRATE);
	cfsetospeed(&newtio,BAUDRATE);
	tcsetattr(fd,TCSANOW,&newtio);
}

void port_close(void) {
	tcsetattr(fd,TCSANOW,&oldtio);
	close(fd);
	fd=-1;
}

int send_cmd(char *cmd) {
	int retval;
	char buffer[256];
	int retries;
	int len=strlen(cmd);
	int i,ok;

	sprintf(buffer,"%c%c%s%c",1,48,cmd,13);
	port_write(buffer,len+3);
	retries=RETRIES;
	while(retries>0) {
		usleep(USLEEP);
		retval=port_read(buffer,256);
		if(retval>0) {
			for(i=0;i<retval;i++) {
				ok=1;
				if(buffer[i]==3) ok=0;
				if(buffer[i]==13) ok=0;
				if(ok) printf("%c",buffer[i]);
			}
			break;
		}
		retries--;
	}
	return retval>0;
}

int main(int argc, char **argv) {
	int len;
	char one,two;

	// ARGUMENTS CHECK
	if(argc!=3) {
		printf("%s device command\n",argv[0]);
		printf("   where command can be:\n");
		printf("   - start: activate the servo feature\n");
		printf("   - stop: deactivate the servo feature\n");
		printf("   - pos: tell position\n");
		printf("   - home: go to home position\n");
		printf("   - move+/move-: do some example movement\n");
		printf("   - other commands are sent directly to the motor controller!!!\n");
		return 0;
	}
	// OPEN PORT
#ifdef DEBUG
	printf("Open %s\n",argv[1]);
#endif
	port_open(argv[1]);
	if(fd==-1) {
		printf("Could not open %s\n",argv[1]);
		return 1;
	}
	// SWITCH COMMAND
	if(strcmp(argv[2],"start")==0) {
		send_cmd("MN"); // SERVO ENABLED
		send_cmd("DP350"); // D-TERM FROM 35 TO 350
	} else if(strcmp(argv[2],"stop")==0) {
		send_cmd("RT"); // RESET
	} else if(strcmp(argv[2],"pos")==0) {
		send_cmd("TT,TP"); // TELL POSITION
	} else if(strcmp(argv[2],"home")==0) {
		//~ send_cmd("GH"); // GOTO HOME
		send_cmd("FE2"); // FIND EDGES
		send_cmd("WS0,DH"); // DEFINE HOME
	} else if(strcmp(argv[2],"move+")==0) {
		send_cmd("MR5000"); // MOVE RELATIVE
	} else if(strcmp(argv[2],"move-")==0) {
		send_cmd("MR-5000"); // MOVE RELATIVE
	} else {
		send_cmd(argv[2]); // OTHER COMMANDS
	}
	// CLOSE PORT
#ifdef DEBUG
	printf("Close %s\n",argv[1]);
#endif
	port_close();
	return 0;
}
