from libc.stdlib cimport malloc, free
from libc cimport errno
from libc.string cimport strerror

cdef extern from "cdb.h":
    ctypedef unsigned int uint32_t
    cdef struct cdb:
        uint32_t dpos
        uint32_t dlen

    void cdb_free(cdb *)
    void cdb_init(cdb *,int fd)

    int cdb_read(cdb *,char *,unsigned int, uint32_t)

    void cdb_findstart(cdb *)
    int cdb_findnext(cdb *,const char *,unsigned int)
    int cdb_find(cdb *,const char *,unsigned int)


cdef extern from "cdb_make.h":
    cdef struct cdb_make:
        int fd

    int cdb_make_start(cdb_make *,int)
    int cdb_make_addbegin(cdb_make *,unsigned int,unsigned int)
    int cdb_make_addend(cdb_make *,unsigned int,unsigned int,uint32_t)
    int cdb_make_add(cdb_make *,const char *,unsigned int,const char *,unsigned int)
    int cdb_make_finish(cdb_make *)


cdef class CDB:
    cdef cdb i
    cdef object file
    cdef str encoding
    cdef int readable

    def __cinit__(self, file, encoding='ascii'):
        self.file = file
        self.encoding = encoding
        cdb_init(&self.i, file.fileno())

    def __dealloc__(self):
        cdb_free(&self.i)

    cdef bytes _chars(self, s):
        if isinstance(s, unicode):
            s = (<unicode>s).encode(self.encoding)
        return s

    property file:
        def __get__(self):
            return self.file

    property encoding:
        def __get__(self):
            return self.encoding

    property dpos:
        def __get__(self):
            return self.i.dpos

    property dlen:
        def __get__(self):
            return self.i.dlen

    def findstart(self):
        cdb_findstart(&self.i)
        self.readable = 0

    def findnext(self, key):
        cdef bytes key_b = self._chars(key)
        cdef int retval = cdb_findnext(&self.i, key_b, len(key_b))
        if retval < 0:
            raise IOError(errno.errno, strerror(errno.errno))
        readable = retval != 0
        self.readable = readable
        return readable

    def read(self, decode=True):
        if not self.readable:
            raise Exception('data is unavailable')
        buf = bytearray(self.i.dlen)
        retval = cdb_read(&self.i, buf, self.i.dlen, self.i.dpos)
        if retval < 0:
            raise IOError(errno.errno, strerror(errno.errno))
        if decode:
            buf = buf.decode(self.encoding)
        return buf

    def readbuf(self, buf, n):
        if not self.readable:
            raise Exception('data is unavailable')
        if n > len(buf):
            n = len(buf)
        if n > self.i.dlen:
            n = self.i.dlen
        if n < 0:
            raise ValueError('n must be equal to or greater than 0')
        retval = cdb_read(&self.i, buf, n, self.i.dpos)
        if retval < 0:
            raise IOError(errno.errno, strerror(errno.errno))
        self.i.dpos += n
        self.i.dlen -= n


cdef class CDBMake:
    cdef cdb_make i
    cdef object file
    cdef str encoding

    def __cinit__(self, file, encoding='ascii'):
        self.file = file
        self.encoding = encoding
        cdb_make_start(&self.i, file.fileno())

    def __dealloc__(self):
        self.finish()

    cdef bytes _chars(self, s):
        if isinstance(s, unicode):
            s = (<unicode>s).encode(self.encoding)
        return s

    property file:
        def __get__(self):
            return self.file

    property encoding:
        def __get__(self):
            return self.encoding

    def finish(self):
        if self.i.fd >= 0:
            if cdb_make_finish(&self.i) < 0:
                raise IOError(errno.errno, strerror(errno.errno))
        self.i.fd = -1

    def add(self, key, data):
        cdef bytes key_b = self._chars(key)
        cdef bytes data_b = self._chars(data)
        cdef int retval = cdb_make_add(&self.i, key_b, len(key_b), data_b, len(data_b))
        if retval < 0:
            raise IOError(errno.errno, strerror(errno.errno))
        return retval == 0
