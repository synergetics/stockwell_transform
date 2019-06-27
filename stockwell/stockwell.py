"""
bindings for libstockwell
"""

from .libstockwell import \
  st as _st, \
  ist as _ist, \
  hilbert as _hilbert, \
  set_wisfile as _set_wisfile, \
  st_freq as _st_freq, \
  sine_taper as _sine_taper

from  .libstockwell import doubleArray


def __cast(arr):
  a = doubleArray(len(arr))
  for i in range(len(arr)):
    a[i] = arr[i]
  return a

def __cast_back(arr, l):
  res = [None] * l
  for i in range(l):
    res[i] = arr[i]
  return res


def st(data, lo=0, hi=0, l=0):
  dat = __cast(data)

  if l == 0: l = len(data)
  if lo == 0 and hi == 0: hi = int(l/2)

  s = (hi - lo + 1) * l
  result = doubleArray(int(s))
  _st(int(l), int(lo), int(hi), dat, result)
  return __cast_back(result, l)

def ist(data, l=0, lo=0, hi=0):
  dat = __cast(data)

  if l == 0: l = len(data)
  if lo == 0 and hi == 0: hi = l/2

  result = doubleArray(l)
  _ist(int(l), int(lo), int(hi), dat, result)
  return __cast_back(result, l)

def hilbert(data, l=0):
  dat = __cast(data)

  if l == 0: l = len(data)

  result = doubleArray(l)
  _hilbert(int(l), dat, result)
  return __cast_back(result, l)

def sine_taper(k, N):
  result = doubleArray(N)
  _sine_taper(int(k), int(N), result)
  return __cast_back(result, N)

def set_wisfile():
  _set_wisfile()


def st_freq(f, l, srate):
  return _st_freq(f, l, srate)

