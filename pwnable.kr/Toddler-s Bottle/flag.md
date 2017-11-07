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
```shell
Noting Important
```
Strings the file 
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $strings flag | more
UPX!
@/x8
gX lw_
H/\_@
	Kl$
H9\$(t
[]]y
nIV,Uh
AWAVAUATS
uSL9
>t		.
```
There is UPX lets see if we can decompress it ..... Bingo Its true UPX decompressed it and we can have readable strings 
Now lets try to decompile the ELF File 
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $r2 flag 
Warning: Cannot initialize dynamic strings
[0x00401058]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Emulate code to find computed references (aae)
[x] Analyze consecutive function (aat)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[0x00401058]> pdf @ sym.main
            ;-- main:
/ (fcn) sym.main 61
|   sym.main ();
|           ; var int local_8h @ rbp-0x8
|              ; DATA XREF from 0x00401075 (entry0)
|           0x00401164      55             push rbp
|           0x00401165      4889e5         mov rbp, rsp
|           0x00401168      4883ec10       sub rsp, 0x10
|           0x0040116c      bf58664900     mov edi, str.I_will_malloc___and_strcpy_the_flag_there._take_it. ; 0x496658 ; "I will malloc() and strcpy the flag there. take it." ; const char * s
|           0x00401171      e80a0f0000     call sym.puts               ; int puts(const char *s)
|           0x00401176      bf64000000     mov edi, 0x64               ; 'd' ; 100 ; size_t size
|           0x0040117b      e850880000     call sym.malloc             ;  void *malloc(size_t size)
|           0x00401180      488945f8       mov qword [local_8h], rax
|           0x00401184      488b15e50e2c.  mov rdx, qword obj.flag     ; [0x6c2070:8]=0x496628 str.UPX...__sounds_like_a_delivery_service_:_ ; "(fI"
|           0x0040118b      488b45f8       mov rax, qword [local_8h]
|           0x0040118f      4889d6         mov rsi, rdx
|           0x00401192      4889c7         mov rdi, rax
|           0x00401195      e886f1ffff     call sub.ifunc_40c050_320
|           0x0040119a      b800000000     mov eax, 0
|           0x0040119f      c9             leave
\           0x004011a0      c3             ret
```
Note There is a String that is passed called obj.flag -> **UPX...__sounds_like_a_delivery_service_:_ ;**
Submitting this says its wrong lets grep the original string 
```shell
┌─[micr0b0t@parrot]─[~/Desktop/pwnable/flag]
└──╼ $strings flag | grep UPX
UPX...? sounds like a delivery service :)
```
And there you have :D 
