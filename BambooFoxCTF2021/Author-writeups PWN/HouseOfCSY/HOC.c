#include<stdlib.h>
#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<pthread.h>
#include<string.h>
#define ROOMNUM 0x20
#define ROOMSIZE 0x5
#define DESTRUCTSLEEP 10
struct ROOM{
    char name[0x20];
    unsigned int user_num;
    char *users[ROOMSIZE];
};
struct ROOM* room[ROOMNUM];

int read_int(int fd)
{
    char tmp[24];
    read(fd, tmp, 23);
    return atoi(tmp);
}

void create_room(int fd)
{
    int idx=0;
    for(;idx<ROOMNUM && room[idx];idx++);
    if(idx >= ROOMNUM){
        dprintf(fd, "Full\n");
        return ;
    }

    room[idx] = (struct ROOM*)malloc(sizeof(struct ROOM));
    room[idx]->user_num = 0x0;
    memset(room[idx]->users, 0, sizeof(room[idx]->users));

    dprintf(fd, "Room name: ");
    size_t inp_len = read(fd, room[idx]->name, 0x20-0x1);
    if(inp_len <= 0){
        dprintf(fd, "Read error\n");
        close(fd);
        pthread_exit(0);
    }
    room[idx]->name[inp_len] = 0;
    dprintf(fd, "Room created!!! Room id: %d\n", idx);
}

void show_room(int fd)
{
    dprintf(fd, "Input index: ");
    unsigned int idx = read_int(fd);
    if(idx>=ROOMSIZE || !room[idx]){
        dprintf(fd, "Bad hacker!!\n");
        //shutdown(fd,SHUT_RDWR);
        close(fd);
        pthread_exit(0);
    }

    dprintf(fd, "Room %s\n", room[idx]->name);
    dprintf(fd, "Users in the room:\n");
    for(int i=0;i<ROOMSIZE;i++){
        if(!room[idx]->users[i]) continue;
        dprintf(fd, "User %s\n", room[idx]->users[i]);
    }
}

void enter_room(int fd)
{
    dprintf(fd, "Which room do you want to enter: ");
    unsigned int idx = read_int(fd);
    if(idx>=ROOMSIZE || !room[idx]){
        dprintf(fd, "Bad hacker!!\n");
        close(fd);
        pthread_exit(0);
    }

    int uidx = 0;
    for(;uidx<ROOMSIZE && room[idx]->users[uidx];uidx++);
    if(uidx>=ROOMSIZE){
        dprintf(fd, "Full\n");
        return ;
    }

    //char *username = (char *)malloc(0x20);
    //room[idx]->users[uidx] = username;
    room[idx]->users[uidx] = (char *)malloc(0x20);
    dprintf(fd, "What's your name: ");
    size_t inp_len = read(fd, room[idx]->users[uidx], 0x20-0x1);
    if(inp_len <= 0){
        dprintf(fd, "Read error\n");
        close(fd);
        pthread_exit(0);
    }
    //dprintf(fd, "Entered\n");
    room[idx]->users[uidx][inp_len] = 0;
    dprintf(fd, "Entered\n");
}

void destruct_room(int fd)
{
    dprintf(fd, "Which room do you want to destruct: ");
    unsigned int idx = read_int(fd);
    if(idx>=ROOMSIZE || !room[idx]){
        dprintf(fd, "Bad hacker!!\n");
        close(fd);
        pthread_exit(0);
    }

    for(int i=0;i<ROOMSIZE;i++){
        if(!room[idx]->users[i]) continue;
        free(room[idx]->users[i]);
        room[idx]->users[i] = 0;
    }
    dprintf(fd, "Destructing...");
    /*for(int i=0;i<DESTRUCTSLEEP;i++){
        dprintf(fd, ".");
        sleep(1);
    }*/
    free(room[idx]);
    room[idx] = 0;
    dprintf(fd, "Destructed\n");
}

void banner(int fd)
{
    dprintf(fd, " ______     ______     __  __    \n");
    dprintf(fd, "/\\  ___\\   /\\  ___\\   /\\ \\_\\ \\   \n");
    dprintf(fd, "\\ \\ \\____  \\ \\___  \\  \\ \\____ \\  \n");
    dprintf(fd, " \\ \\_____\\  \\/\\_____\\  \\/\\_____\\ \n");
    dprintf(fd, "  \\/_____/   \\/_____/   \\/_____/ \n");
    dprintf(fd, "                                 \n");
}

void menu(int fd)
{
    dprintf(fd, "------ House Of CSY ------\n");
    dprintf(fd, "| 1. Create a room       |\n");
    dprintf(fd, "| 2. Show a room         |\n");
    dprintf(fd, "| 3. Enter a room        |\n");
    dprintf(fd, "| 4. Destruct a room     |\n");
    dprintf(fd, "--------------------------\n");
    dprintf(fd, "Choose> ");
}

void *handler(void *socket_fd)
{
    int fd = *(int *)socket_fd;
    banner(fd);
    while(1){
        menu(fd);
        int ch = read_int(fd);
        switch(ch){
            case 1:
                create_room(fd);
                break;
            case 2:
                show_room(fd);
                break;
            case 3:
                enter_room(fd);
                break;
            case 4:
                destruct_room(fd);
                break;
            default:
                dprintf(fd, "Invalid choose\n");
                break;
        }
    }
}

int main(){
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd == -1){
        puts("Couldn't create socket.");
        exit(-1);
    }

    struct sockaddr_in server_info;
    server_info.sin_family = AF_INET;
    server_info.sin_addr.s_addr = inet_addr("0.0.0.0");
    server_info.sin_port = htons( 54321 );

    if( bind(socket_fd, (struct sockaddr*)&server_info, sizeof(server_info)) < 0 ){
        puts("Bind error");
        exit(-1);
    }

    if( listen(socket_fd, 5) == -1 ){
        puts("Listen error");
        exit(-1);
    }

    int client_fd;
    struct sockaddr_in client_info;
    int addr_len = sizeof(client_info);
    pthread_t thread_id;
    while( client_fd = accept(socket_fd, (struct sockaddr*)&client_info, &addr_len) ){
        printf("New connection from %s, socket fd is %d\n", inet_ntoa(client_info.sin_addr), client_fd);
        if( pthread_create(&thread_id, NULL, handler, (void *)&client_fd) ){
            puts("Thread create error");
        }
    }
    return 0;
}