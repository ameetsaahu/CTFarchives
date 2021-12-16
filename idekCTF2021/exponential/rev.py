from pwn import *

context.log_level = "ERROR"

flag = "p"

c1s = 'rR'
for c1 in c1s:
	c2s = 'eE3'
	for c2 in c2s:
		c3s = 'cC'
		for c3 in c3s:
			c4s = 'iI1'
			for c4 in c4s:
				c5s = 's5S'
				for c5 in c5s:
					c6s = 'eE3'
					for c6 in c6s:
						c7s = '_'
						for c7 in c7s:
							input = flag + c1 + c2 + c3 + c4 + c5 + c6 + c7
							target = process(["./reverseme", input])
							print input
							res = target.recvline()
							res += target.recvline()
							print res
							if "Loop" in res:
								flag += chr(c1+1) + chr(c2+2)
								print "Flag: " + flag
								target.close()
								exit()
							else:
								target.close()
								'''
							c7 = chr(ord(c7)+1)
						c6 = chr(ord(c6)+1)
					c5 = chr(ord(c5)+1)
				c4 = chr(ord(c4) + 1)
			c3 = chr(ord(c3) + 1)
		c2 = chr(ord(c2) + 1)
	c1 = chr(ord(c1) + 1)
'''