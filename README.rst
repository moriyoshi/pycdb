pycdb
=====

pycdb is yet another binding of CDB, a constant database implementation created by D. J. Bernstein.

This features portability (works well both with Python 2.x and Python 3.x), restriction-free license (public domain), reentrancy.


Synopsis
--------

::

    from pycdb import CDBMake, CDB
    
    w = CDBMake(open('test.cdb', 'wb'), encoding='utf-8')
    w.add('a', '1')
    w.add('b', '2')
    w.add('c', '3')
    w.finish()
    
    r = CDB(open('test.cdb', 'rb'), encoding='utf-8')
    print(r['a']) # '1'
    print(r['b']) # '2'
    print(r['c']) # '3'
