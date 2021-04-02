#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <seccomp.h>
#include <sys/utsname.h>

char* ptr[4] = {0, 0, 0, 0};
int seccomped=0;

void sandbox() {
  if (!seccomped) {
    scmp_filter_ctx seccomp_ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(seccomp_ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_load(seccomp_ctx);
    seccomp_release(seccomp_ctx);
  }
  seccomped=1;
}

void setup() {
  setvbuf(stdin,NULL,_IONBF,0);
  setvbuf(stderr,NULL,_IONBF,0);
  setvbuf(stdout,NULL,_IONBF,0);
}

int auth() {
  char login[16] = {0};
  char password[16] = {0};
  char user_login[16] = {0};
  char user_password[16] = {0};
  int fd = open("auth.txt", O_RDONLY);
  char buf[100] = {0};
  read(fd, buf, 100);
  strncpy(login, buf, strchr(buf, ':')-buf);
  strncpy(password, strchr(buf, ':')+1, strchr(buf, '\n')-strchr(buf, ':')-1);
  puts("Login:");
  read(0, user_login, 16);
  puts("Password:");
  read(0, user_password, 16);
  for (int i = 0; i < 5; i++) {
    if (!strchr(login, user_login[i])) {
      return 0;
    }
  }
  for (int i = 0; i < 6; i++) {
    if (!strchr(password, user_password[i])) {
      return 0;
    }
  }
  return 1;
}

int get_game_number() {
  char num[16] = {0};
  int number = 0;
  puts("Input your game's number:");
  read(0, num, 16);
  number = atoi(num);
  if (number >= 1 && number <= 4) {
    return number;
  } else {
    puts("Invalid number");
    return -1;
  }
}

void create() {
  int number = get_game_number();
  if (number != -1) {
    if (!ptr[number-1]) {
      ptr[number-1] = (char*)calloc(1, 0x100);
      puts("Tell about it:");
      read(0, ptr[number-1], 0x50);
      puts("OK. Got your thoughts.");
      return;
    }
  }
}

void print() {
  int number = get_game_number();
  if (number != -1) {
    if (ptr[number-1]) {
      puts("Content:");
      puts(ptr[number-1]);
    }
  }
  return;
}

void delet() {
  int number = get_game_number();
  if (number != -1) {
    if (ptr[number-1]) {
      free(ptr[number-1]);
      ptr[number-1] = 0;
    }
  }
}

void upload() {
  char buf[16] = {0};
  puts("Input your size:");
  read(0, buf, 16);
  read(0, buf, atoi(buf));
  puts(buf);
  return;
}

int menu() {
  char buf[16] = {0};
  puts("1. Create game");
  puts("2. Print game\n3. Delete game");
  puts("4. Upload file\n5. Test RNG");
  puts("6. Exit\nYour choice:");
  read(0, buf, 16);
  return atoi(buf);
}

int try_rng() {
  char buf[16] = {0};
  int number=0;
  srand(time(NULL));
  int r = rand()%100;
  puts("Type your guess:");
  read(0, buf, 16);
  number = atoi(buf);
  if (number == r) {
    puts("Hooray! You're real lucky boy");
  } else {
    printf("Nah. The correct one is %d\n", r);
  }
  return r;
}

void finish() {
  exit(0);
}

int main() {
  setup();
  sandbox();
  if (!auth()) {
    return 1;
  }
  for (;;) {
     switch (menu()) {
       case 1:
        create();
        break;
      case 2:
        print();
        break;
      case 3:
        delet();
        break;
       case 4:
        upload();
        break;
      case 5:
        try_rng();
        break;
      case 6:
        finish();
        break;
     };
  }
}
