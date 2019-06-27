#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension

import sys,os
import numpy.core

NUMPYDIR = os.path.dirname(numpy.core.__file__)

# linux first
if sys.platform=='linux' or sys.platform=='linux2':
    include_dirs = [os.path.join(NUMPYDIR, r'include/numpy')]
    libraries=['fftw3']
    library_dirs=[] # assume we use default locations

if sys.platform=='win32':
    library_dirs = [r"c:\pythonxy\local\bin"] # to pick up fftw3
    include_dirs = [os.path.join(NUMPYDIR, r'include/numpy'), r"c:\pythonxy\local\include"]
    libraries=['fftw3-3']

stext = Extension("st", sources=["stockwell/st.c"],
    libraries=libraries,
    include_dirs=include_dirs,
    library_dirs=library_dirs)

setup(
  name = 'stockwell',
  version="0.0.5",
  ext_modules = [stext],
)
