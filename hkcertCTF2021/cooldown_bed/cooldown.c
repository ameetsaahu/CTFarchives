#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(60);
}

int main () {
    char buf[100];
    char end[8] = "N";
    init();
    printf("Welcome to echo service.\n");
    while(!(end[0] == 'Y' || end[0] == 'y')){
        int num_read = read(0, buf, 0x100);
        if (buf[num_read-1] == '\n')
            buf[num_read-1] = '\0';
        printf("%s", buf);
        printf("End?[Y/N] ");
        scanf("%7s", end);
    }
}