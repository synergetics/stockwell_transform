import setuptools
from distutils.core import setup
from distutils.extension import Extension
import sys,os
import numpy.core

NUMPYDIR = os.path.dirname(numpy.core.__file__)

# linux first
if sys.platform=='linux2':
    include_dirs = [os.path.join(NUMPYDIR, r'include/numpy')]
    libraries=['fftw3']
    library_dirs=[] # assume we use default locations
    
if sys.platform=='win32':
    library_dirs = [r"c:\pythonxy\local\bin"] # to pick up fftw3
    include_dirs = [os.path.join(NUMPYDIR, r'include/numpy'), r"c:\pythonxy\local\include"]
    libraries=['fftw3-3']

stext = Extension("stockwell.st", ["stockwell/stmodule.c", "stockwell/st.c"], 
    libraries=libraries,
    include_dirs=include_dirs,
    library_dirs=library_dirs)
    
sineext= Extension("stockwell.sine", ["stockwell/sinemodule.c"], include_dirs=include_dirs)
ext_modules_stockwell=[stext,sineext]

setup(
  name = 'stockwell',
  version="0.0.4",
  packages=["stockwell"],
  ext_modules = ext_modules_stockwell,
)
