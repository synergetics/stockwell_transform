#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension

import sys,os
import numpy.core

import re
import requests
import numpy

# download numpy.i
np_version = re.compile(r'(?P<MAJOR>[0-9]+)\.'
            '(?P<MINOR>[0-9]+)') \
            .search(numpy.__version__)
np_version_string = np_version.group()
np_version_info = {key: int(value)
           for key, value in np_version.groupdict().items()}

np_file_name = 'numpy.i'
np_file_url = 'https://raw.githubusercontent.com/numpy/numpy/maintenance/' + \
        np_version_string + '.x/tools/swig/' + np_file_name
if(np_version_info['MAJOR'] == 1 and np_version_info['MINOR'] < 9):
  np_file_url = np_file_url.replace('tools', 'doc')

chunk_size = 8196
with open(np_file_name, 'wb') as file:
  for chunk in requests.get(np_file_url,
                stream=True).iter_content(chunk_size):
    file.write(chunk)


NUMPYDIR = os.path.dirname(numpy.core.__file__)

if sys.platform=='linux' or sys.platform=='linux2':
    include_dirs = [os.path.join(NUMPYDIR, r'include/numpy'), '.']
    libraries=['fftw3', 'm']
    library_dirs=[numpy.get_include()] # assume we use default locations

ext = Extension(
  '_libstockwell',
  sources=['stockwell/stockwell_wrap.c', 'stockwell/st.c', 'stockwell/sine.c'],
  include_dirs=include_dirs,
  library_dirs=library_dirs,
  libraries=libraries
)

setup(
  name = 'stockwell',
  version="0.1.0",
  ext_modules = [ext],
  py_modules = ["stockwell/stockwell"],
  include_package_data=True,
  packages=['stockwell'],
  include_dirs=[numpy.get_include()]
)

