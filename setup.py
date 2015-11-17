import os
from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = lambda arg: arg

setup(
    name='pycdb',
    version='0.0.0',
    description='Yet another CDB wrapper',
    url='http://github.com/moriyoshi/pycdb',
    author='Moriyoshi Koizumi',
    author_email='mozo@mozo.jp',
    license='public domain',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Database',
        'License :: Public Domain',
        ],
    packages=['pycdb'],
    ext_modules=cythonize([
        Extension(
            'pycdb._pycdb',
            include_dirs=['pycdb'],
            sources=[
                os.path.join('pycdb', file_)
                for file_ in [
                    '_pycdb.pyx',
                    'alloc.c',
                    'buffer.c',
                    'buffer_2.c',
                    'buffer_put.c',
                    'byte_copy.c',
                    'byte_cr.c',
                    'byte_diff.c',
                    'cdb.c',
                    'cdb_hash.c',
                    'cdb_make.c',
                    'error.c',
                    'error_str.c',
                    'fmt_ulong.c',
                    'scan_ulong.c',
                    'seek_cur.c',
                    'seek_set.c',
                    'str_len.c',
                    'uint32_pack.c',
                    'uint32_unpack.c',
                    ]
                ]
            )
        ]),
    test_suite='pycdb',
    zip_safe=False
    )
