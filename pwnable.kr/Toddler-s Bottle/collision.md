Challenge Description

```text
Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```
Lets Connect and See What we go 

```shell
┌─[✗]─[microbot@parrot]─[~]
└──╼ $ssh col@pwnable.kr -p2222
col@pwnable.kr's password: 
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
Last login: Wed Oct 11 12:05:19 2017 from 79.51.158.233
col@ubuntu:~$ ls -l
total 16
-r-sr-x--- 1 col_pwn col     7341 Jun 11  2014 col
-rw-r--r-- 1 root    root     555 Jun 12  2014 col.c
-r--r----- 1 col_pwn col_pwn   52 Jun 11  2014 flag
```
Running the executable **col**

```shell
col@ubuntu:~$ ./col
usage : ./col [passcode]
col@ubuntu:~$ ./col 123456
passcode length should be 20 bytes
```
Lets see the code 

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```

So The Challenge Says Hash Collision it has nothing to do with MD5 Hash Collision but same concept sending a string to the 
program when it pass to some process it generate the same hash as **0x21DD09EC**

Reading the Code we see that there were *character* pointer in **check_password** was casted to *int* pointer

The Trick here is as follows the *int* block is 4 bytes while the *chr* block is 1 byte and the required password is 20 char
which is 5 bytes 

In another word we need to add 5 blocks of characters to have **0x21DD09EC** as output 

to do so we can do the following

```python
col@ubuntu:~$ python
Python 2.7.12 (default, Jul  1 2016, 15:12:24) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> hex(0x21DD09EC /5)
'0x6c5cec8'
>>> hex(0x21DD09EC - (0x6c5cec8 * 4))
'0x6c5cecc'
```
we divided the value of the hashcode to 5 we have the first 4 bytes of the password and now subtract the 4 bytes from the 
original hash to get the last 4 bytes of the password to fit in 20 characters -> 5 bytes 

another Note: the system is using Little Endian so the bytes are reversed , Now lets inject it to the app

```shell
col@ubuntu:~$ ./col `python -c "print('\xc8\xce\xc5\x06'*4 +'\xcc\xce\xc5\x06')"`
daddy! I just managed to create a hash collision :)
```

