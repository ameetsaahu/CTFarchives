#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <stdint.h>
#include <signal.h>
#include <seccomp.h>

pid_t child_pid;

int child_main() {
  return printf("Child: %p\n", malloc(0x80));
}

int parent_main() {
  return printf("Child: %p\n", malloc(0x80));
}

int main() {
  
  setvbuf(stdin,0,2,0);
  setvbuf(stderr,0,2,0);

  child_pid = fork();
  if(child_pid == -1) {
    perror("Error Fork.\n");
    exit(-1);
  }
  if(child_pid == 0) {
    child_main();
  } else {
    parent_main();
  }
  exit(0);
}
