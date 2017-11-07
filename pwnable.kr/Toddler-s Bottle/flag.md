Challenge 
```text
Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary
```
now lets run it and see what it do 
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $./flag
bash: ./flag: Permission denied
┌─[✗]─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $chmod +x flag 
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $./flag 
I will malloc() and strcpy the flag there. take it.
```
Lets Check with ltrace what happen 
