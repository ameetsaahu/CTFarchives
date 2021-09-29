res = "\x48\x73\x76\x04\x74\x6a\x61\x06\x05\x59\x62\x73\x76\x5c\x54\x14\x41\x59\x58\x41\x05\x6a\x58\x76\x06\x4e\x61\x59\x58\x61\x00"

for c in res:
	c = chr(ord(c) ^ 0x35)

print res

s2 = [0]
for i in range(0x1e):
	s2.append(0)

print s2

n = 0x1e
j = 0
i = 0
while j < n:
	s2[j] = ord(res[i])
	i = i + 1
	j = j + 2

k = 1
while k < n:
	s2[k] = ord(res[i])
	i = i + 1
	k = k + 2

rev = ""
for l in s2:
	rev += chr(l)

print rev
