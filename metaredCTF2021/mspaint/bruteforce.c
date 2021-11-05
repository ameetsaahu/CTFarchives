#include <stdio.h>
#include <stdlib.h>

#define N 10

int main()
{
	int seed, nums, leaks[N], i;
	int s;
	for (i = 0 ; i < N ; i++)	scanf("%d", &leaks[i]);

	for (s = 0x700 ; s < 0x100000000 ; s+=0x1000)
	{
		srand(s);
		for (i = 0 ; i < N ; i++)
		{
			if ((int)rand() != leaks[i])	break;
		}
		if (i == N)	return printf("%d\n%d\n", s, rand());
	}
	if (s >= 0x100000000)	printf("%d\n%d\n", s, rand());
	return printf("%d\n%d\n", -1, rand());
}
