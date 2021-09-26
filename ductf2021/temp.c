#include <stdio.h>

int main()
{
	int a;
	printf("User Input: ");
	scanf("%d", &a);

	if (a >= 30 && a <= 50)		puts("Average");
	else if (a > 50 && a <= 60)	puts("Good");
	else if (a > 60 && a <= 80)	puts("Excellent");
	else if (a > 80 && a <= 100)puts("Outstanding");
	return 0;
}