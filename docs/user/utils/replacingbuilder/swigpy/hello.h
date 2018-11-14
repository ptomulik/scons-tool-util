#ifndef HELLO_H
#define HELLO_H

#ifdef _WIN32
# ifdef BUILDING_HELLO
#  define HELLO_API __declspec(dllexport)
# else
#  define HELLO_API __declspec(dllimport)
# endif
#else
# define HELLO_API
#endif

#ifdef __cplusplus
extern "C" {
#endif

extern void HELLO_API hello();

#ifdef __cplusplus
}
#endif
#endif
