#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(){

    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    char path[0x10] = {0};
    char *argv[5] = {NULL, NULL, NULL, NULL, NULL};
    char *envp[5] = {NULL, NULL, NULL, NULL, NULL};

    for (int i = 0; i < 4; i++){
        argv[i] = (char *)malloc(0x20);
        envp[i] = (char *)malloc(0x40);
    }

    printf("[+] enter path : ");
    scanf("%15s", path);
    puts("[+] enter argv (use NULL to stop) (4 at max)");
    for(int i = 0; i < 4; i++){
        printf("argv[%d] : ", i);
        scanf("%31s", argv[i]);
        
        if (strcmp(argv[i], "NULL") == 0){
            argv[i] = NULL;
            break;
        }
    }

    puts("[+] enter envp (use NULL to stop) (4 at max)");
    for(int i = 0; i < 4; i++){
        printf("envp[%d] : ", i);
        scanf("%63s", envp[i]);

        if (strcmp(envp[i], "NULL") == 0){
            envp[i] = NULL;
            break;
        }
    }

    if (strstr(path, "sh")){
        puts("[-] Shell Not Allowed");
        _exit(-1);
    }

    if (strstr(argv[0], "sh")){
        puts("[-] Shell Not Allowed");
        _exit(-1);
    }
   

    puts("[+] executing your commands!");
    printf("execve(\"%s\", [", path);
    int i = 1;
    for (char * temp = argv[0]; temp != NULL; temp = argv[i], i++){

        if (argv[0] == NULL){
            break;
        }
        printf("\"%s\", ", temp);
    }

    i = 1;
    for (char * temp = envp[0]; i < 4 && temp != NULL; temp = envp[i], i++){}

    printf("NULL], %p /* %d vars */)\n", envp, i-1);

    execve(path, argv, envp);

    return 0;
}
