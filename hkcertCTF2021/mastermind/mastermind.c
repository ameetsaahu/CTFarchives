#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_SIZE 26
#define min(a, b) ((a)<(b)?(a):(b))

typedef struct Context Context;
typedef struct Game Game;
typedef struct Record Record;
typedef struct Layout Layout;

struct Record {
    int red_peg;
    int white_peg;
    char *trial;
};

struct Game {
    int round;
    int endgame_round;
    Record **records;
};

struct Context {
    Game game;
    char *tokenset;
    char *answer;
    int size;
    FILE *urandom;
};

struct Layout {
    char board[0x1000];
    char line_format[32];
    char head_format[32];
    char body_format[32];
    char padding[MAX_SIZE];
};

Context context;

void _abort(char* msg) {
    printf("%s", msg);
    exit(1);
}

int read_int() {
    char buf[16];
    int num_read = read(0, buf, 15);
    if (num_read <= 0)
        _abort("input error!\n");
    if (buf[num_read-1] == '\n')
        buf[num_read-1] = '\0';
    return atoi(buf);
}

void read_all(int len, char *buf) {
    while (1) {
        int num_read = read(0, buf, len);
        if (num_read <= 0)
            _abort("input error!\n");
        for (int i = num_read-1; i>=0 ; i--) {
            if (buf[i] == '\n') {
                buf[i] = '\0';
                num_read--;
            }
        }
        if (num_read == len) {
            buf[len] = '\0';
            break;
        }
        printf("Your guess should be in lenght %d.\n", len);
    }
    getc(stdin);
}

int count(char *buf, char token) {
    int count = 0;
    while(*buf) {
        if (*buf == token)
            count++;
        buf++;
    }
    return count;
}

void generate_answer() {
    char temp_buf[0x100];
    int random;
    memset(temp_buf, '\0', 0x100);

    for (int i = 0; i < context.size; i++) {
        fread(&random, 1, 1, context.urandom);
        random %= context.size;
        temp_buf[i] = context.tokenset[random];
    }

    context.answer = strdup(temp_buf);
    if (context.answer == NULL)
        _abort("strdup error!\n");
}

void generate_tokenset() {
    char temp_buf[0x100];

    strncpy(temp_buf, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", context.size);

    context.tokenset = strdup(temp_buf);
    if (context.tokenset == NULL)
        _abort("strdup error!\n");
}

void init_game() {
    context.game.round = 0;
    context.game.endgame_round = context.size*2 + 2;
    void* chunk = malloc(sizeof(Record*) * (context.game.endgame_round));
    if (chunk == NULL)
        _abort("malloc error!\n");
    context.game.records = (Record **)chunk;
    for (int i = 0; i < context.game.endgame_round; i++) {
        void* record = malloc(sizeof(Record));
        if (record == NULL)
            _abort("malloc error!\n");
        context.game.records[i] = (Record*) record;
        context.game.records[i]->red_peg = 0;
        context.game.records[i]->white_peg = 0;
    }
}

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
    alarm(600);
    printf("Welcome to MasterMind.\n");
    printf("Tell me the size of gameboard:");
    context.size = read_int();
    if ((context.size <= 0) || (context.size > MAX_SIZE))
        _abort("invalid game size!\n");
    context.urandom = fopen("/dev/urandom", "r");
    if (context.urandom == NULL)
        _abort("open error!\n");
    generate_tokenset();
    generate_answer();
    init_game();
}

void pad(char *padding, char padding_char, int size) {
    memset(padding, '\0', MAX_SIZE);
    if (size <= 0)
        return;
    memset(padding, padding_char, size);
}

void print_board() {

    Layout layout;

    strcpy(layout.line_format, "%s--------------------%s\n");
    strcpy(layout.head_format, "%s|Round|Input%s|Reward|\n");
    strcpy(layout.body_format, "%s|%02i   |%s%s|R%02iW%02i|\n");

    pad(layout.padding, '-', context.size - 5);
    sprintf(layout.board, layout.line_format, layout.board, layout.padding);
    pad(layout.padding, ' ', context.size - 5);
    sprintf(layout.board, layout.head_format, layout.board, layout.padding);
    pad(layout.padding, '-', context.size - 5);
    sprintf(layout.board, layout.line_format, layout.board, layout.padding);

    for (int i = 0; i < context.game.round; i++) {
        pad(layout.padding, ' ', 5 - context.size);
        sprintf(layout.board, layout.body_format, layout.board, i, context.game.records[i]->trial, layout.padding,
         context.game.records[i]->red_peg, context.game.records[i]->white_peg);
        pad(layout.padding, '-', context.size - 5);
        sprintf(layout.board, layout.line_format, layout.board, layout.padding);
    }
    
    printf("\n%s\n", layout.board);
        
    layout.board[0] = '\0';
}

int play_round() {
    char guess[MAX_SIZE+1]; 
    int correct = 0;
    int red_peg = 0;
    int white_peg = 0;
    printf("[%d] Guess(A-%c){%d}:", context.game.round, 'A' + context.size - 1, context.size);
    read_all(context.size, guess);
    for (int i = 0; i < context.size; i++)
        white_peg += min(count(guess, context.tokenset[i]), count(context.answer, context.tokenset[i]));
    for (int i = 0; i < context.size; i++)
        if (guess[i] == context.answer[i])
            red_peg ++;
    white_peg -= red_peg;
    context.game.records[context.game.round]->red_peg = red_peg;
    context.game.records[context.game.round]->white_peg = white_peg;
    context.game.records[context.game.round]->trial = strdup(guess);
    correct = (strcmp(guess, context.answer) == 0);
    if (correct)
        return 1;
    return 0;
}

void play() {
    int ending = 0;
    while (ending != 1) {
        print_board();
        if (context.game.round == context.game.endgame_round) {
            printf("Bye bye!\n");
            exit(0);
        }
        ending = play_round();
        context.game.round++;
        if (ending == 1)
            printf("Congrat! You win the game!\n");
        else {
            for (int i = 0; i < 8; i++) {
                printf(".");
                // usleep(50*1000);
            }
            printf("\n");
        }
    }
}

int main() {
    init();
    play();
}   