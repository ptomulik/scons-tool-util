#ifdef _WIN32
# include <windows.h>
typedef HINSTANCE lib_t;
# define OpenLib(_s) LoadLibrary(_s)
# define OpenLib_str "LoadLibrary"
# define LoadLibSym(_lib,_s) GetProcAddress(_lib, _s)
# define LoadLibSym_str "GetProcAddress"
#else
# include <dlfcn.h>
typedef void* lib_t;
# define OpenLib(_s) dlopen(_s, RTLD_NOW)
# define OpenLib_str "dlopen"
# define LoadLibSym(_lib,_s) dlsym(_lib,_s)
# define LoadLibSym_str "dlsym"
#endif

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32

void error_exit(LPTSTR func)
{
    // Retrieve the system error message for the last-error code

    LPVOID msg;

    FormatMessageA( FORMAT_MESSAGE_ALLOCATE_BUFFER |
                    FORMAT_MESSAGE_FROM_SYSTEM |
                    FORMAT_MESSAGE_IGNORE_INSERTS,
                    NULL,
                    GetLastError(),
                    MAKELANGID(LANG_ENGLISH, SUBLANG_ENGLISH_US),
                    (LPTSTR) &msg,
                    0, NULL );
    fprintf(stderr, "%s() failed: %s\r\n", func, (LPTSTR)msg);
    LocalFree(msg);

    exit(EXIT_FAILURE);
}

#else

void error_exit(char const* func)
{
    fprintf(stderr, "%s() failed: %s\n", func, dlerror());
    exit(EXIT_FAILURE);
}

#endif

typedef void(*void_fcn_t)();

void_fcn_t load_hello_wrap()
{
  void_fcn_t hello_wrap;
  lib_t pyd = OpenLib("_hello.pyd");
  if(!pyd) {
    error_exit(OpenLib_str);
  }
  hello_wrap = (void_fcn_t)LoadLibSym(pyd, "hello_wrap");
  if(!hello_wrap) {
    error_exit(LoadLibSym_str);
  }
  return hello_wrap;
}

int main(int argc, const char* argv[])
{
  void_fcn_t hello_wrap = load_hello_wrap();
  hello_wrap();
  return 0;
}
