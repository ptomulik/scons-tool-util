#ifdef _WIN32
# include <windows.h>
#else
# include <dlfcn.h>
#endif
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

typedef void(*void_fcn_t)();

void_fcn_t load_hello_wrap()
{
  void_fcn_t hello_wrap;
#ifdef _WIN32
  HINSTANCE dll = LoadLibrary("_hello.pyd");
  if(!dll) {
    fprintf(stderr, "LoadLibrary() failed: %s\n", GetLastError());
    exit(EXIT_FAILURE);
  }
  hello_wrap = (void_fcn_t)GetProcAddress(dll, "hello_wrap");
  if(!hello_wrap) {
    fprintf(stderr, "GetProcAddress() failed: %s\n", GetLastError());
    exit(EXIT_FAILURE);
  }
#else
  void *so = dlopen("_hello.pyd", RTLD_NOW);
  if(!so) {
    fprintf(stderr, "dlopen() failed: %s\n", dlerror());
    exit(EXIT_FAILURE);
  }
  hello_wrap = (void_fcn_t)dlsym(so, "hello_wrap");
  if(!hello_wrap) {
    fprintf(stderr, "dlsym() failed: %s\n", dlerror());
    exit(EXIT_FAILURE);
  }
#endif
  return hello_wrap;
}

int main(int argc, const char* argv[])
{
  void_fcn_t hello_wrap = load_hello_wrap();
  hello_wrap();
  return 0;
}
