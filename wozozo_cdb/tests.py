import os
import unittest
import tempfile

class CDBMakeTest(unittest.TestCase):
    def setUp(self):
        fd, self.file = tempfile.mkstemp()
        self.f = os.fdopen(fd, 'wb+')

    def tearDown(self):
        self.f.close()
        os.unlink(self.file)

    def test_open(self):
        from wozozo_cdb import CDBMake
        CDBMake(self.f)

    def test_finish_idempotency(self):
        from wozozo_cdb import CDBMake
        c = CDBMake(self.f)
        c.finish()
        v = self.f.tell()
        c.finish()
        self.assertEqual(self.f.tell(), v)
        c.finish()
        self.assertEqual(self.f.tell(), v)

    def test_add(self):
        from wozozo_cdb import CDBMake
        c = CDBMake(self.f)
        self.assertTrue(c.add('test', 'test'))
        c.finish()

class CDBTest(unittest.TestCase):
    def setUp(self):
        fd, self.file = tempfile.mkstemp()
        self.f = os.fdopen(fd, 'wb+')

    def tearDown(self):
        self.f.close()
        os.unlink(self.file)

    def test_it(self):
        from wozozo_cdb import CDB
        import base64
        import zlib
        testdata = base64.b64decode(b'eJwT4GAAA4FRetDRTEBaAcofpUfpUXqUHqVHaWrSLFBcklpcAsIMUGC8vriGAagGADizKiQ=')
        self.f.write(zlib.decompress(testdata))
        self.f.seek(0, 0)
        x = CDB(self.f)
        x.findstart()
        self.assertFalse(x.findnext('none'))
        x.findstart()
        self.assertTrue(x.findnext('test'))
        self.assertEqual(x.dpos, 2060)
        self.assertEqual(x.dlen, 4)
        b = bytearray(10)
        self.assertEqual(x.read(), 'test')
        

