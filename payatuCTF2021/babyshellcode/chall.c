#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>

int main(){

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    char * shellcode = mmap ( NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    
    // read shellcode
    printf("[+] Shellcode : ");
    int len = read(0, shellcode, 0x1000);
    for (int i = 0; i < len; i++){
        if (shellcode[i] == 'H'){
            fprintf(stderr, "[-] 0ops, 64 bit shellcode found! EXITING ...\n");
            _exit(-1);
        }
    }

    (*(void (*)())shellcode)();
}
