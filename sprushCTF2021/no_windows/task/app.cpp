#include <Windows.h>
#include <stdio.h>
#include <vector>
#include <fcntl.h>
#include <io.h>
#include <stdlib.h>
#include <stdio.h>
#include <share.h>
#include <winbase.h>
#include <process.h>
#include "difichento.h"
using namespace std;

#define ALLOC_COUNT 10
#define BUFFER_SIZE 40

void setup() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
}

int readfile(const char* str, char* stor) {
  HANDLE hFile = INVALID_HANDLE_VALUE;
  DWORD dwBytesRead = 0;
  hFile = CreateFile(str,
                     GENERIC_READ,
                     FILE_SHARE_READ,
                     NULL,
                     OPEN_EXISTING,
                     FILE_ATTRIBUTE_NORMAL,
                     NULL);
   if (hFile == INVALID_HANDLE_VALUE) {
     printf("Can't open %s\n", str);
     return -1;
   }
   if(ReadFile(hFile, stor, (BUFFER_SIZE-1), &dwBytesRead, NULL)== FALSE) {
     printf("Can't read %s\n", str);
     CloseHandle(hFile);
     return 1;
   }
   if (dwBytesRead > 0) {
     stor[dwBytesRead]='\0';
   }
   CloseHandle(hFile);
   return 0;
}

void menu() {
  puts("1. Create difichento");
  puts("2. Call difichento");
  puts("3. Make difichento tell something");
  puts("4. Delete game");
  puts("5. Edit game");
  puts("6. Print game");
  puts("7. Exit");
  printf("\n>> ");
}

int get_id() {
  int choice;
  printf("Input id>> ");
  scanf("%d", &choice);
  return choice;
}

int main() {
  void* ptr;
  void* str_allocations[10] = {0};
  Difichento* obj_arr[10] = {0};
  int choice = 0;
  Difichento* dif_ptr;
  int cur_index = 0;

  setup();
  for (int i = 0; i < ALLOC_COUNT; i++) {
    ptr = malloc(100);
    memset(ptr, 0x41+i, 100);
    str_allocations[i] = ptr;
  }
  for (;;) {
    menu();
    scanf("%d", &choice);
    switch (choice) {
      case 1:
        if (cur_index >= 9) {
          break;
        }
        puts("[1] Ivan");
        puts("[2] Fedot");
        puts("[3] Evkakiy");
        choice = get_id();
        switch (choice) {
          case 1:
            obj_arr[cur_index] = new Ivan();
            cur_index++;
            break;
          case 2:
            obj_arr[cur_index] = new Fedot();
            cur_index++;
            break;
          case 3:
            obj_arr[cur_index] = new Evkakiy();
            cur_index++;
            break;
          default:
            break;
        }
        break;
      case 2:
        choice = get_id();
        if ((choice >= 0) && (choice < 10) && obj_arr[choice]) {
          obj_arr[choice]->say();
        }
        break;
      case 3:
        choice = get_id();
        if ((choice >= 0) && (choice < 10) && obj_arr[choice]) {
          obj_arr[choice]->tell(obj_arr[choice]->speech);
        }
        break;
      case 4:
        choice = get_id();
        if (str_allocations[choice])
          free(str_allocations[choice]);
        break;
      case 5:
        choice = get_id();
        if (str_allocations[choice]) {
          write(1, ">> ", 3);
          _read(0, str_allocations[choice], 100);
        }
        break;
      case 6:
        choice = get_id();
        if (str_allocations[choice]) {
          write(1, str_allocations[choice], 100);
          puts("");
        }
        break;
      case 7:
        exit(0);
      default:
        break;
    }
  }
}
