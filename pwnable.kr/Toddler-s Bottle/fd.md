Challenge 

```text
Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner,
follow this tutorial link: https://www.youtube.com/watch?v=blAxTfcW9VU

ssh fd@pwnable.kr -p2222 (pw:guest)
```
Conecting 

```shell
┌─[microbot@parrot]─[~]
└──╼ $ssh fd@pwnable.kr -p2222
The authenticity of host '[pwnable.kr]:2222 ([143.248.249.64]:2222)' can't be established.
ECDSA key fingerprint is SHA256:kWTx0QCL5U5VbUkQa1x5/dw8hJ6DS5CR0KilMRJnUYY.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[pwnable.kr]:2222,[143.248.249.64]:2222' (ECDSA) to the list of known hosts.
fd@pwnable.kr's password: 
 ____  __    __  ____    ____  ____   _        ___      __  _  ____  
|    \|  |__|  ||    \  /    ||    \ | |      /  _]    |  |/ ]|    \ 
|  o  )  |  |  ||  _  ||  o  ||  o  )| |     /  [_     |  ' / |  D  )
|   _/|  |  |  ||  |  ||     ||     || |___ |    _]    |    \ |    / 
|  |  |  `  '  ||  |  ||  _  ||  O  ||     ||   [_  __ |     \|    \ 
|  |   \      / |  |  ||  |  ||     ||     ||     ||  ||  .  ||  .  \
|__|    \_/\_/  |__|__||__|__||_____||_____||_____||__||__|\_||__|\_|
                                                                     
- Site admin : daehee87.kr@gmail.com
- IRC : irc.netgarage.org:6667 / #pwnable.kr
- Simply type "irssi" command to join IRC now
- files under /tmp can be erased anytime. make your directory under /tmp
- to use peda, issue `source /usr/share/peda/peda.py` in gdb terminal
Last login: Wed Oct 11 11:10:35 2017 from 114.124.133.52
```
Listing Files See if we have anything interesting 

```shell
fd@ubuntu:~$ ls
fd  fd.c  flag
fd@ubuntu:~$ ls -la
total 40
drwxr-x---  5 root   fd   4096 Oct 26  2016 .
drwxr-xr-x 80 root   root 4096 Jan 11  2017 ..
d---------  2 root   root 4096 Jun 12  2014 .bash_history
-r-sr-x---  1 fd_pwn fd   7322 Jun 11  2014 fd
-rw-r--r--  1 root   root  418 Jun 11  2014 fd.c
-r--r-----  1 fd_pwn root   50 Jun 11  2014 flag
-rw-------  1 root   root  128 Oct 26  2016 .gdb_history
dr-xr-xr-x  2 root   root 4096 Dec 19  2016 .irssi
drwxr-xr-x  2 root   root 4096 Oct 23  2016 .pwntools-cache
fd@ubuntu:~$ cat flag.c
cat: flag.c: No such file or directory
fd@ubuntu:~$ cat fd.c 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
```
Now we have **0x1234 = 4660 decemial** now if we insert this number will lead **fd = 0** so the buffer will ask **stdin** for data 
To Get a Close look on what happen before we enter the Pass 

This is the Linux File IO that it was saying to look for and also the read function 

```c
read(int fildes, void *buf, size_t nbytes);
```
in the read function the fildes we can use 0 1 2 to use the linux IO streams and below what are those streams

```text
Streams

Input and output in the Linux environment is distributed across three streams. These streams are:

    standard input (stdin)

    standard output (stdout)

    standard error (stderr)

The streams are also numbered:

    stdin (0)

    stdout (1)

    stderr (2)
```
now we can pass **LETMEWIN** Then we have our flag 

```shell
fd@ubuntu:~$ ./fd 4670
learn about Linux file IO
fd@ubuntu:~$ ./fd 4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```
