#include <stdio.h>      // puts(), printf(), scanf(), fflush()
#include <stdlib.h>     // exit() atoi()
#include <string.h>     // memset(), strlen(), strcmp()
#include <stdbool.h>    // bool

void ___syscall_malloc(void) {
  puts("Nope.");
  exit(1);
}

void ____syscall_malloc(void) {
  puts("Good job.");
  return;
}

int main(void) {
  int     n;
  char    input[31];
  char    key[9];
  size_t  input_index;
  size_t  key_index;
  size_t  temp1;
  int     temp3;
  size_t  temp2;
  bool    temp4;
  char    number[4];

  printf("Please enter key: ");
  n = scanf("%30s", input);
  if (n != 1) {
    ___syscall_malloc();
  }
  if (input[0] != '4') {
    ___syscall_malloc();
  }
  if (input[1] != '2') {
    ___syscall_malloc();
  }
  fflush(stdin);
  memset(key, 0, 9);    // key = 000 000 000
  key[0] = '*';         // key = *00 000 000

  number[3] = 0;
  input_index = 2;
  key_index = 1;

  while (true) {
    temp2 = strlen(key);
    temp1 = input_index;
    temp4 = false;

    if (temp2 < 8) {
      temp2 = strlen(input);
      temp4 = temp1 < temp2;
    }
    if (!temp4) {
      break;
    }

    number[0] = input[input_index];
    number[1] = input[input_index + 1];
    number[2] = input[input_index + 2];

    temp3 = atoi(number);
    key[key_index] = (char)temp3;

    input_index = input_index + 3;
    key_index = key_index + 1;
  }

  key[key_index] = '\0';
  n = strcmp(key, "********");

  if (n == -2) {
    ___syscall_malloc();
  }
  else if (n == -1) {
    ___syscall_malloc();
  }
  else if (n == 0) {
    ____syscall_malloc();
  }
  else if (n == 1) {
    ___syscall_malloc();
  }
  else if (n == 2) {
    ___syscall_malloc();
  }
  else if (n == 3) {
    ___syscall_malloc();
  }
  else if (n == 4) {
    ___syscall_malloc();
  }
  else if (n == 5) {
    ___syscall_malloc();
  }
  else if (n == 0x73) {
    ___syscall_malloc();
  }
  else {
    ___syscall_malloc();
  }

  return 0;
}
