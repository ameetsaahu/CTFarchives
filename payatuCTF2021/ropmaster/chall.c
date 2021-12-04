#include <stdio.h>

int get_numbers(int * buffer, int size){
    int *curr = buffer;

    // if previous number is 0x13377331 then stop taking input
    while (curr < buffer + size && *(curr-1) != 0x13377331){
        scanf("%d", curr++);
    }

    return 0;
}

int main(){
    int numbers[0x100] = {0};
    return get_numbers(numbers, sizeof(numbers));
}
