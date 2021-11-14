from pwn import *

elf = ELF("./service")

target = elf.process()
#target = remote("chalp.hkcert21.pwnable.hk", 28015)

name = "b"*31
target.sendline(name)

gdb.attach(target, 'b strcpy\nc\nc')

for i in range(256):
	target.sendlineafter(">", "hkcert21{" + str(i) + "}")

target.interactive()