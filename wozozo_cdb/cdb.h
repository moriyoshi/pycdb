/* Public domain. */

#ifndef CDB_H
#define CDB_H

#include "uint32.h"

#define CDB_HASHSTART 5381
extern uint32_t cdb_hashadd(uint32_t,unsigned char);
extern uint32_t cdb_hash(char *,unsigned int);

struct cdb {
  char *map; /* 0 if no map is available */
  int fd;
  uint32_t size; /* initialized if map is nonzero */
};

struct cdb_cursor {
  uint32_t loop; /* number of hash slots searched under this key */
  uint32_t khash; /* initialized if loop is nonzero */
  uint32_t kpos; /* initialized if loop is nonzero */
  uint32_t hpos; /* initialized if loop is nonzero */
  uint32_t hslots; /* initialized if loop is nonzero */
  uint32_t dpos; /* initialized if cdb_findnext() returns 1 */
  uint32_t dlen; /* initialized if cdb_findnext() returns 1 */
} ;

extern void cdb_free(struct cdb *);
extern void cdb_init(struct cdb *,int fd);

extern int cdb_read(struct cdb *,char *,unsigned int,uint32_t);

extern void cdb_findstart(struct cdb *, struct cdb_cursor *);
extern int cdb_findnext(struct cdb *,struct cdb_cursor *,char *,unsigned int);

#define cdb_datapos(c) ((c)->dpos)
#define cdb_datalen(c) ((c)->dlen)

#endif
