#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//flag = pesuctf{fl3g15go2d}

char output[] = "2svj153vum";
int len; 

int main()
{
	int i, j, k;
	len = strlen(output);
	char s[len+1];
	char flag[len+1];
	for (i=0;i<len+1;i++)	s[i] = 0;
	for (i=0;i<len+1;i++)	flag[i] = 0;
	j = 0;
	k = len + -2;
	while (-1 < k) 
	{
		s[j] = output[k];
		s[j+1] = output[k+1];
		j = j + 2;
		k = k + -2;
	}
	for (i=0;i<len+1;i++)
	{
		if (i==1 || i==7)	flag[i] = 0x7a - (s[i] - '_');
		else if ((s[i] < 'a') || ('z' < s[i]))	
			flag[i] = s[i];
		else flag[i] = s[i] - 0xf;
	}
	for (i=0;i<len+1;i++)	printf("%c", flag[i]);
	puts("");
	return 0;
}
