#ifdef _WIN32
# include <windows.h>
#else
# include <dlfcn.h>
#endif
#include <stddef.h>
#include <stdio.h>

typedef void(*void_fcn_t)();

int main(int argc, const char* argv[])
{
  void_fcn_t hello_wrap = NULL;
#ifdef _WIN32
  HINSTANCE dll = LoadLibrary("_hello.pyd");
  if(!dll) {
    fprintf(stderr, "LoadLibrary failed: %s\n", GetLastError());
    return 1;
  }
  hello_wrap = (void_fcn_t)GetProcAddress(dll, "hello_wrap");
#else
  void *so = dlopen("./_hello.pyd", RTLD_NOW);
  if(!so) {
    fprintf(stderr, "dlopen failed: %s\n", dlerror());
    return 1;
  }
  dlerror();
  hello_wrap = (void_fcn_t)dlsym(so, "hello_wrap");
#endif
  hello_wrap();
  return 0;
}
