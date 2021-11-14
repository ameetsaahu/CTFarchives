#include <stdio.h>

#define max 0x80000000-1

int main()
{
	int offset, epos, count;
	offset = max;
	count = max;
	printf("%x\n", (epos = offset + count));
	return 0;
}