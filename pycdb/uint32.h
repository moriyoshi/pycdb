#ifndef UINT32_H
#define UINT32_H

#include <stdint.h>

extern void uint32_pack(char *,uint32_t);
extern void uint32_pack_big(char *,uint32_t);
extern void uint32_unpack(char *,uint32_t *);
extern void uint32_unpack_big(char *,uint32_t *);

#endif
