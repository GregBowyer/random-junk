#!/usr/bin/tcc -run
#include <stdio.h>

/**
 * TCC RULES!
 */
int main(int argc, char** argv) { 
    printf("Hello there, how are you doing you persistent little node ? \n");

    printf("I got %d arguments, isnt that really kw00t\n", argc);

    if(argc < 2) {
        printf("I give up, you are no fun feed me files paths !\n");
        return 1;
    }

    int i = 0;

    for(i = 0; i < argc; i++) {
        printf("i is %d\n", i);
        printf("Humm and the arg of the day is .... %s\n", argv[i]);
    }

    return 0;
}
