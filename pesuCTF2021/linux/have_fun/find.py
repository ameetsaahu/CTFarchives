from pwn import *

target = process('./script.sh')

target.recvuntil("ctf{")
print(target.recv(60))


