#ifndef HELLO_WRAP_H
#define HELLO_WRAP_H

#ifdef _WIN32
# ifdef BUILDING_HELLO_WRAP
#  define HELLO_WRAP_API __declspec(dllexport)
# else
#  define HELLO_WRAP_API __declspec(dllimport)
# endif
#else
# define HELLO_WRAP_API
#endif

#ifdef __cplusplus
extern "C" {
#endif

extern void HELLO_WRAP_API hello_wrap();

#ifdef __cplusplus
}
#endif

#endif /* HELLO_WRAP_H */
