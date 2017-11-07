Mommy told me to make a passcode based login system.
My initial C code was compiled without any error!
Well, there was some compiler warning, but who cares about that?

ssh passcode@pwnable.kr -p2222 (pw:guest)

lets Connect and see what do we have 

```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $ssh passcode@pwnable.kr -p2222
The authenticity of host '[pwnable.kr]:2222 ([143.248.249.64]:2222)' can't be established.
ECDSA key fingerprint is SHA256:kWTx0QCL5U5VbUkQa1x5/dw8hJ6DS5CR0KilMRJnUYY.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[pwnable.kr]:2222,[143.248.249.64]:2222' (ECDSA) to the list of known hosts.
passcode@pwnable.kr's password: 
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
Last login: Tue Nov  7 08:40:02 2017 from 159.149.191.123
passcode@ubuntu:~$ ls -la
total 36
drwxr-x---  5 root passcode     4096 Oct 23  2016 .
drwxr-xr-x 80 root root         4096 Jan 11  2017 ..
d---------  2 root root         4096 Jun 26  2014 .bash_history
-r--r-----  1 root passcode_pwn   48 Jun 26  2014 flag
dr-xr-xr-x  2 root root         4096 Aug 20  2014 .irssi
-r-xr-sr-x  1 root passcode_pwn 7485 Jun 26  2014 passcode
-rw-r--r--  1 root root          858 Jun 26  2014 passcode.c
drwxr-xr-x  2 root root         4096 Oct 23  2016 .pwntools-cache
```
so we have 3 files important to us **flag** **passcode** **passcode.c**

Running passcode
```shell
passcode@ubuntu:~$ cat flag 
cat: flag: Permission denied
passcode@ubuntu:~$ ./passcode 
Toddler's Secure Login System 1.0 beta.
enter you name : microbot
Welcome microbot!
enter passcode1 : 123
Segmentation fault
```
lets go ahead and read passcode.c
```c
passcode@ubuntu:~$ cat passcode.c 
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}
```
Re Compiling the Source code shows 2 errors 
```shell
passcode@ubuntu:~$ gcc passcode.c 
passcode.c: In function ‘login’:
passcode.c:9:8: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat=]
  scanf("%d", passcode1);
        ^
passcode.c:14:15: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat=]
         scanf("%d", passcode2);
               ^
/usr/bin/ld: cannot open output file a.out: Permission denied
collect2: error: ld returned 1 exit status
```
Lets see whats inside ltrace
```shell
passcode@ubuntu:~$ ltrace ./passcode 
__libc_start_main(0x8048665, 1, 0xffe0f5a4, 0x80486a0 <unfinished ...>
puts("Toddler's Secure Login System 1."...Toddler's Secure Login System 1.0 beta.
)                                                                                                        = 40
printf("enter you name : ")                                                                                                                        = 17
__isoc99_scanf(0x80487dd, 0xffe0f478, 0xf76d7d60, 0xf759171benter you name : something
)                                                                                      = 1
printf("Welcome %s!\n", "something"Welcome something!
)                                                                                                               = 19
printf("enter passcode1 : ")                                                                                                                       = 18
__isoc99_scanf(0x8048783, 0xf758702b, 0, 0xf76d7d60enter passcode1 : 10
 <no return ...>
--- SIGSEGV (Segmentation fault) ---
+++ killed by SIGSEGV +++
```
lets debug the code, i will compile it and add some debugging statements
so it crashed after this line **scanf("%d", passcode1);**
when i did this test case
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/passcode]
└──╼ $./test1 
Toddler's Secure Login System 1.0 beta.
enter you name : something
Welcome something!
enter passcode1 : 123
Segmentation fault
```
and passed it when i did the below test case so i know its character that is looking for 
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/passcode]
└──╼ $./test1
Toddler's Secure Login System 1.0 beta.
enter you name : a
Welcome a!
enter passcode1 : a
you Entered this pass : 21880enter passcode2 : checking...
Login Failed!
```
So I have added the second debug statment below this line **scanf("%d", passcode2);** to print what is passcode2
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/passcode]
└──╼ $./test2 
Toddler's Secure Login System 1.0 beta.
enter you name : as
Welcome as!
enter passcode1 : d
you Entered this pass1 : 22048
enter passcode2 : you Entered this pass2 : -423307520
 checking...
Login Failed!
```
**NOTE** Above Case i entered 1 character ended up pass2 is -ve number but below is more than 1 character and i have +ve value
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/passcode]
└──╼ $./test2 
Toddler's Secure Login System 1.0 beta.
enter you name : as
Welcome as!
enter passcode1 : asd
you Entered this pass1 : 22010
enter passcode2 : you Entered this pass2 : 894801664
 checking...
Login Failed!
```
So Now its Clear we need to find the proper combiniation to get the flag time to brute force the service 
We need **passcode1==338150 && passcode2==13371337**

A Different Way of thinking , lets not try to brute force the passcode but lets try to use the code vulnerability since its
giving segmentation fault 

Pause Here and I need to learn GDB 
