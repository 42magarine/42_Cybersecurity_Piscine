#include <stdio.h>      // puts(), printf(), scanf(), fflush()
#include <stdlib.h>     // exit() atoi()
#include <string.h>     // memset(), strlen(), strcmp()
#include <stdbool.h>    // bool

void no(void) {
  puts("Nope.");
  exit(1);
}

void ok(void) {
  puts("Good job.");
  return;
}

int main(void) {
  int     n;
  char    input[24];
  char    key[9];
  size_t  input_index;
  size_t  key_index;
  size_t  temp1;
  size_t  temp2;
  int     temp3;
  bool    temp4;
  char    number[4];

  printf("Please enter key: ");
  n = scanf("%23s", input);
  if (n != 1) {
    no();
  }
  if (input[0] != '0') {
    no();
  }
  if (input[1] != '0') {
    no();
  }
  fflush(stdin);
  memset(key, 0, 9);  // key = 000 000 000
  key[0] = 'd';       // key = d00 000 000

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
  temp3 = strcmp(key, "delabere");

  if (temp3 == 0) {
    ok();
  }
  else {
    no();
  }

  return 0;
}
