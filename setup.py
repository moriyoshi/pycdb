import os
from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = lambda arg: arg

setup(
    name='wozozo-cdb',
    version='0.0.0',
    description='Yet another CDB wrapper',
    url='http://github.com/moriyoshi/wozozo-cdb',
    author='Moriyoshi Koizumi',
    author_email='mozo@mozo.jp',
    license='public domain',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Database',
        'License :: Public Domain',
        ],
    packages=['wozozo_cdb'],
    ext_modules=cythonize([
        Extension(
            'wozozo_cdb._wozozo_cdb',
            include_dirs=['wozozo_cdb'],
            sources=[
                os.path.join('wozozo_cdb', file_)
                for file_ in [
                    '_wozozo_cdb.pyx',
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
    test_suite='wozozo_cdb',
    zip_safe=False
    )
