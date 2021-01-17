from pwn import *
target = process('./script.sh')

while True:
	c = target.recv(1)
#	print("I'm up...")
	if c.isupper():
		print c
