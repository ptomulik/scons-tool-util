#include "hello.h"
#include "hello_wrap.h"
#include <stdio.h>
void HELLO_WRAP_API hello_wrap() {
  printf("wrap" EOL "  ");  fflush(stdout);
  hello();
  printf("unwrap" EOL);     fflush(stdout);
}
