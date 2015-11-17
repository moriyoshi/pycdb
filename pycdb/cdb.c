/* Public domain. */

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include "readwrite.h"
#include "error.h"
#include "seek.h"
#include "byte.h"
#include "cdb.h"

void cdb_free(struct cdb *c)
{
  if (c->map) {
    munmap(c->map,c->size);
    c->map = 0;
  }
}

void cdb_findstart(struct cdb *c, struct cdb_cursor *cur)
{
  cur->loop = 0;
}

void cdb_init(struct cdb *c,int fd)
{
  struct stat st;
  char *x;

  cdb_free(c);
  c->fd = fd;

  if (fstat(fd,&st) == 0)
    if (st.st_size <= 0xffffffff) {
      x = mmap(0,st.st_size,PROT_READ,MAP_SHARED,fd,0);
      if (x + 1) {
	c->size = st.st_size;
	c->map = x;
      }
    }
}

int cdb_read(struct cdb *c,char *buf,unsigned int len,uint32_t pos)
{
  if (c->map) {
    if ((pos > c->size) || (c->size - pos < len)) goto FORMAT;
    byte_copy(buf,len,c->map + pos);
  }
  else {
    if (seek_set(c->fd,pos) == -1) return -1;
    while (len > 0) {
      int r;
      do
        r = read(c->fd,buf,len);
      while ((r == -1) && (errno == error_intr));
      if (r == -1) return -1;
      if (r == 0) goto FORMAT;
      buf += r;
      len -= r;
    }
  }
  return 0;

  FORMAT:
  errno = error_proto;
  return -1;
}

static int match(struct cdb *c,char *key,unsigned int len,uint32_t pos)
{
  char buf[32];
  int n;

  while (len > 0) {
    n = sizeof buf;
    if (n > len) n = len;
    if (cdb_read(c,buf,n,pos) == -1) return -1;
    if (byte_diff(buf,n,key)) return 0;
    pos += n;
    key += n;
    len -= n;
  }
  return 1;
}

int cdb_findnext(struct cdb *c,struct cdb_cursor *cur,char *key,unsigned int len)
{
  char buf[8];
  uint32_t pos;
  uint32_t u;

  if (!cur->loop) {
    u = cdb_hash(key,len);
    if (cdb_read(c,buf,8,(u << 3) & 2047) == -1) return -1;
    uint32_unpack(buf + 4,&cur->hslots);
    if (!cur->hslots) return 0;
    uint32_unpack(buf,&cur->hpos);
    cur->khash = u;
    u >>= 8;
    u %= cur->hslots;
    u <<= 3;
    cur->kpos = cur->hpos + u;
  }

  while (cur->loop < cur->hslots) {
    if (cdb_read(c,buf,8,cur->kpos) == -1) return -1;
    uint32_unpack(buf + 4,&pos);
    if (!pos) return 0;
    cur->loop += 1;
    cur->kpos += 8;
    if (cur->kpos == cur->hpos + (cur->hslots << 3)) cur->kpos = cur->hpos;
    uint32_unpack(buf,&u);
    if (u == cur->khash) {
      if (cdb_read(c,buf,8,pos) == -1) return -1;
      uint32_unpack(buf,&u);
      if (u == len)
	switch(match(c,key,len,pos + 8)) {
	  case -1:
	    return -1;
	  case 1:
	    uint32_unpack(buf + 4,&cur->dlen);
	    cur->dpos = pos + 8 + len;
	    return 1;
	}
    }
  }

  return 0;
}
