import os
from setuptools import setup, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = lambda arg: arg

setup(
    name='pycdb',
    version='0.0.1',
    description='Yet another CDB wrapper',
    url='http://github.com/moriyoshi/pycdb',
    author='Moriyoshi Koizumi',
    author_email='mozo@mozo.jp',
    license='public domain',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'License :: Public Domain',
        ],
    long_description = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.rst'))).read(),
    packages=['pycdb'],
    keywords=['cdb', 'cython'],
    install_requires=[],
    extra_require={
        'dev': ['cython'],
        },
    package_data={
        'pycdb': [
            'alloc.h',
            'buffer.h',
            'byte.h',
            'cdb.h',
            'cdb_make.h',
            'error.h',
            'fmt.h',
            'readwrite.h',
            'scan.h',
            'seek.h',
            'str.h',
            'uint32.h',
            ],
        },
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
