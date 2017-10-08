Connecting to the service shows 4 types of question "min,max,sum,avg"


```python
from pwn import *

def solver(q,arr):
    arr.sort()
    print("arr After Sort ",arr)
    print("arr length " ,len(arr))
    if "max" in q:
        maximum = arr[-1]
        return maximum
    elif "min" in q:
        minimum = arr[0]
        return minimum
    elif "sum" in q:
        s = 0
        for i in arr:
            s = s + i
        return s
    elif "avg" in q:
        avg = 0
        for i in arr:
            avg = avg + i
        avg = avg / float(len(arr))
        return avg


r = remote("92.222.90.84",5003)
task = r.recvrepeat(10)
print(task)
while(True):
    task = task.split("\n")
    arr = task[0]
    question = task[1]
    arr = arr.split(" ")
    if arr == " " or arr == "":
        r.send("0\n")
    else:
        for i in range(0,len(arr)):
            arr[i] = int(arr[i])
        result = solver(question,arr)
        print(result)
        r.send(str(result)+"\n")
    task =r.recvrepeat(10)
    print(task)
```
The Output is :

```shell
Welcome Euclid!
The flag is: pwnerrank{i_th0ugh7_u_c0uldnt_d0_m47h}
```
