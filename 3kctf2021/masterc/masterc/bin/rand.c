#include <stdio.h>
#include <time.h>

int main()
{
	srand(time(0));
	int i = 0;
	while(i++ < 10)
	{
		printf("%ld\n", rand());
	}
}