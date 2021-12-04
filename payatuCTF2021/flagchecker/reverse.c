// flag{1_h0p3_y0u_d1d_n0t_s0lv3_it_by_h4nd}
#include <stdio.h>
#include <string.h>

char enc[] = "\x85\x85\x8c\x82\xf6\xb0\x4a\x81\xab\xf1\xa6\x7a\xe8\xa9\xe8\x4a\x47\x38\x43\xea\x75\x39\x73\x6a\x3e\x31\x6b\x37\x2e\xd2\xdc\xdd\xd2\x87\x34\xca\x3b\xfd\x3d\x7d\x5c";

int main()
{
	int i = 0, j;
	unsigned int p_int;
	char flag[0x50] = {0}, temp;
	for (i = 0; i<strlen(enc) ; i++)
	{
		for (j = 0 ; j < 0x100 ; j++)
		{
			temp = (((i - ((i + 0x21) - j ^ i) ^ 0xa2) - 0x2d ^ 0x3c) - i) + -1;
			if (temp == enc[i])
				break;
		}
		if (j == 0x100)
		{
			printf("Couldn't find at index: %d\n", i);
			exit(0);
		}
		flag[i] = j;
	}
	puts(flag);
	return 0;
}
