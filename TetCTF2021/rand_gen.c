#include <stdio.h>
#include <stdlib.h>

int main()
{
	int r1, r2, r3;
	int i = 0;
	scanf("%d %d %d", &r1, &r2, &r3);
	for (i=0;i<=0xffffff;i++)
	{
		srand(i);
		if (r1 == rand())	if (r2 == rand())	if (r3 == rand())
		{
			rand();
			printf("%p\n", rand());
			printf("%p\n", rand());
			printf("The seed found is %p\n", i);
			return 0;
		}
	}
	return 0;
}

/*
int main()
{
	char s[8];
	int i = 0;
	FILE * fp;
	for (;i<8;i++)	s[i] = 0;
	
	for (i=0; i<10000; i++)
	{
		fp = open("/dev/urandom", 0);
		read(fp, s, 3);
		printf("%p\n", *(long *)s);
		close(fp);
	}
}
*/
