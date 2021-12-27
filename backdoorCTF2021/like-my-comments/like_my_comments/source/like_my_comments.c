#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>

#define MAJOR_NUMBER 489

#define IOCTL_CALL _IOWR(MAJOR_NUMBER,0,char *)

struct comment {
    char *comment_string;
    unsigned long long *likes;
};

void get_input(char *buf, size_t len) {
    fgets(buf, len, stdin);
    char *ch;
    if ((ch = strchr(buf, '\n')))
        *ch = '\0';
}

#define BUF_LENGTH 0x100
char inp_buf[BUF_LENGTH];

int main(void) {
    int dev_fd = open("/dev/like", O_RDONLY);
    printf("Hello, World! %lu\n", IOCTL_CALL);

    unsigned long long likes = 0;
    struct comment c = {
        "Some Quote",
        &likes
    };

    printf("Likes for %s : %llu\n", c.comment_string, *c.likes);
    while(1) {
        printf("Want to like this comment more? [y/n]: ");
        get_input(inp_buf, BUF_LENGTH);
        if (inp_buf[0] == 'n' || inp_buf[1] == 'N')
            break;
        ioctl(dev_fd, IOCTL_CALL, &c);
        printf("Likes for %s : %llu\n", c.comment_string, *c.likes);
    }

    printf("Bye, Hope to see you soon\n");
    close(dev_fd);
    return 0;
}

__attribute__((constructor))
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}


