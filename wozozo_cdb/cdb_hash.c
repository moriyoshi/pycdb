/* Public domain. */

#include "cdb.h"

uint32_t cdb_hashadd(uint32_t h,unsigned char c)
{
  h += (h << 5);
  return h ^ c;
}

uint32_t cdb_hash(char *buf,unsigned int len)
{
  uint32_t h;

  h = CDB_HASHSTART;
  while (len) {
    h = cdb_hashadd(h,*buf++);
    --len;
  }
  return h;
}
