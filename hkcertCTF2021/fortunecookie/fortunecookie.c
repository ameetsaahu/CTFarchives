#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SIZE 32


char* msg[MAX_SIZE];
int msg_size[MAX_SIZE];
FILE *urandom;
long long cookie_num = 0;

void _abort(char* msg) {
    printf("%s", msg);
    exit(1);
}

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(60);
    urandom = fopen("/dev/urandom", "r");
    if (urandom == NULL)
        _abort("open error!\n");

    msg[0] = strdup("The best thing to do first thing in the morning is go right back to sleep.");
    msg_size[0] = 0x50;
    msg[1] = strdup("Every 60 seconds in africa a minute passes.");
    msg_size[1] = 0x30;
    msg[2] = strdup("Monday hates you, too.");
    msg_size[2] = 0x18;
    msg[3] = strdup("Money is not everything. There's always credit cards.");
    msg_size[3] = 0x38;
    msg[4] = strdup("Sometimes you don't work hard,you don't know what is despair.");
    msg_size[4] = 0x40;

    cookie_num += 5;
}

void create_cookie() {
    long long size;
    char* message;

    if (cookie_num >= MAX_SIZE)
        _abort("Too many cookie in the box >_<\n");


    printf("How long is the message?");    
    scanf("%lld", &size);

    if (size > 0x100)
        _abort("Too long!\n");


    message = (char*) calloc (size,sizeof(char));

    printf("Input your message: ");    
    int num_read = read(0, message, size);
    if (message[num_read] == '\n')
        message[num_read] = '\0';

    msg[cookie_num] = message;
    msg_size[cookie_num] = size;
    printf("Done!\n\n");    
    cookie_num++;
}

void eat_cookie() {
    int random;
    if (cookie_num == 0)
        _abort("No cookie!\n");
    fread(&random, 1, 1, urandom);
    random %= cookie_num;
    printf("%s\n\n", msg[random]);
    free(msg[random]);
    msg[random] = msg[cookie_num-1];
    msg_size[random] = msg_size[cookie_num-1];
    cookie_num--;
}

void edit_cookie() {
    long long idx;
    
    printf("Which cookie?[0-%d]: ", cookie_num-1);
    scanf("%llu", &idx);

    if (idx >= cookie_num) {
        _abort("Invalid index!");
    }

    printf("New Message: ");

    int num_read = read(0, msg[idx], msg_size[idx]-1);
    if (msg[idx][num_read] == '\n')
        msg[idx][num_read] = '\0';
    printf("Done!\n\n");

}

void read_cookie() {
    long long idx;
    
    printf("Which cookie?[0-%d]: ", cookie_num-1);
    scanf("%llu", &idx);

    if (idx >= cookie_num) {
        _abort("Invalid index!");
    }

    printf("%s\n\n", msg[idx]);
}

void menu() {
    printf("==Fortune Cookie==\n");
    printf("1. Eat one cookie!!\n");
    printf("2. Make new cookie.\n");
    printf("3. Edit cookie msg.\n");
    printf("4. View cookie msg.\n");
    printf("5. exit\n");
    printf("==================\n>\n");
}

int main() {
    long choice;
    init();
    
    while (1){
        menu();
        scanf("%lld", &choice);
        if (choice == 1){
            eat_cookie();
        } else if (choice == 2)
        {
            create_cookie();
        } else if (choice == 3)
        {
            edit_cookie();
        } else if (choice == 4)
        {
            read_cookie();
        } else if (choice == 5)
        {
            exit(0);
        } 
    }

}