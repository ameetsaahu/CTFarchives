#include<stdio.h>

char encoded[] = "\x45\x6E\x74\x65\x72\x5F\x66\x6C\x61\x67\x3A\x5F\x6E\x14\x50\x72\x74\x6D\x44\x44\x7D\x2B\x43\x40\x4C\x40\x4B\x75\x19\x4A\x2A\x1E\x19\x4E\x4F\x2B\x47\x2F\x56\x2D\x18\x77\x43\x03\x0B\x07\x18\x05\x00\x17\x1B\x03\x06\x09\x0F\x19\x12\x1A\x0C\x08\x0D\x01\x02\x11\x1E\x1D\x0E\x10\x04\x15\x13\x14\x1C\x1F\x0A\x16";

char inst[] = "\x01\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x0C\x26\x00\x01\x01\x00\x00\x01\x00\x00\x01\x01\x00\x00\x00\x20\x27\x00\x01\x06\x02\x02\x01\x00\x00\x01\x01\x00\x01\x01\x00\x00\x00\x2C\x2E\x01\x02\x02\x01\x01\x2E\x00\x01\x01\x03\x00\x00\x00\x13\x2E\x03\x02\x01\x01\x00\x01\x00\x00\x2E\x01\x02\x02\x01\x01\x06\x01\x03\x03\x00\x01\x04\x02\x2D\x02\x00\x00\x00\x20\x11\x00\x00\x10\x21\x06\x02\x02\x01\x00\x00\x00\x00\x0C\x2E\x00\x02\x02\x00\x00\x01\x01\x00\x01\x01\x00\x2E\x01\x02\x02\x01\x01\x2C\x00\x01\x0D\x00\x00\x10\xA5\x04\x02\x2D\x02\x00\x00\x00\x20\x11\x00\x00\x10\x61\x01\x00\x00\x00\x00\x4C\x01\x01\x00\x00\x00\x0D\x26\x00\x01\x01\x00\x00\x00\x00\x00\xFF\x00";

char flag[32];

int ptr[4] = {0};

#define p1 ptr[inst[ip+1]]
#define p2 ptr[inst[ip+2]]

int getn(int num)
{
	int ans;
	ans = (num & 0xff)<<24 + (num&0xff00)<<8 + (num&0xff0000)>>8 + num>>24;
	return ans;
}

int main()
{
	int ip = 0;
	char b3 = 0, b4 = 0;
	while(1)
	{
		switch(inst[ip])
		{
			case 1:
				ptr[inst[ip + 1]] = getn(inst[ip+2]);
				ip += 6;
				break;

			case 2:
				if (ptr[inst[ip+2]] < 0x10000)		ptr[inst[ip+1]] = *(int *)(encoded + ptr[inst[ip+2]]);
				else ptr[inst[ip+1]] = *(int *)(flag + ptr[inst[ip+2]] - 0x10000);
				ip += 3;
				break;

			case 3:
				if (ptr[inst[ip+1]] < 0x10000)		*(int *)(flag + ptr[inst[ip+1]]) = ptr[inst[ip+2]];
				else *(int *)(flag + ptr[inst[ip+1]] - 0x10000) = ptr[inst[ip+2]];
				ip += 3;
				break;

			case '&':
				write(1, encoded + ptr[inst[ip+1]], ptr[inst[ip+2]]);
				ip += 3;
				break;

			case 0x27:
				read(0, flag, p2);
				ip += 3;
				break;

			case 6:
				p1 = p1 ^ p2;
				ip += 3;
				break;

			case 'a':
				p1 = getn(inst[ip+2]);
				ip += 6;
				break;

			case '.':
				p1 = p1 + p2;
				ip += 3;
				break;

			case 4:
				p1 = p1 + 1;
				ip += 2;
				break;

			case 0x2c:
				if (p1 == p2)		{b4 = 0; b3 = 1;}
				else if (p1 > p2)	{b4 = 1; b3 = 0;}
				else {b4 = 0; b3 = 0;}
				ip += 3;
				break;

			case 0x2d:
				if (p1 == getn(inst[ip+2]))		{b4 = 0; b3 = 1;}
				else if (p1 > getn(inst[ip+2]))	{b4 = 1; b3 = 0;}
				else {b4 = 0; b3 = 0;}
				ip += 6;
				break;

			//case 0x11:



		}
	}


	return 0;
}


//Instructions
/*
01 00 00 00 00 00
01 01 00 00 00 0C
26 00 01
01 00 00 01 00 00
01 01 00 00 00 20
27 00 01
06 02 02
01 00 00 01 01 00
01 01 00 00 00 2C
2E 01 02
02 01 01
2E 00 01
01 03 00 00 00 13
2E 03 02
01 01 00 01 00 00
2E 01 02
02 01 01
06 01 03
03 00 01
04 02
2D 02 00 00 00 20
11 00 00 10 21
06 02 02
01 00 00 00 00 0C
2E 00 02
02 00 00
01 01 00 01 01 00
2E 01 02
02 01 01
2C 00 01
0D 00 00 10 A5
04 02
2D 02 00 00 00 20
11 00 00 10 61
01 00 00 00 00 4C
01 01 00 00 00 0D
26 00 01
01 00 00 00 00 00
FF 00 01 00 00 00 00 59 01 01 00 00 00 0E 26 00 01 01 00 00 00 00 01 FF 00 FE
*/