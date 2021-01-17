f = open("flag", "r")
flag = ""
n=0
while True:
	c = f.read(1)
	if (c == " "):
		n = n+1
		continue
	if (c == "\n"):
		flag += chr(n)
		n = 0
		continue
	break

print(flag)
