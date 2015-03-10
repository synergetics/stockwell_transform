Stockwell Transform
======

## Contains
1. c code
- python module

## Requirements for compilation

fftw3 libraries
a C compiler (tested with gcc so far)
numpy (tested with 1.3)


see also
Code from Dr. Stockwell's web site for the stockwell transform

http://www.cora.nwra.com/~stockwel/index.php?module=fatcat&fatcat[user]=viewCategory&fatcat_id=2&module_title=pagemaster

Stockwell, R.G, L mansinha, and R. P. Lowe. Localization of the complex spectrum: The S-Transform. IEEE Transactions on Signal Processing, 44(4) pp998--1001, 1996.

## Usage

```python

from pylab import *

# The way the basic module works is, for a signal x
y = stockwell.smt.st(x)
# will return its complex valued transform
# the amplitude "spectra" can be obtained with

ampy = abs(y)

# The rows in the interval [0,n/2) label the number of cycles during
# the entire period of x (ie, it uses the length L of x as the longest
# time)

# So, to covert this back to hz
# Let
# Fs=<sampling interval in Hz>

# Let
Tn = float(L * Fs) # total time, say in seconds, of x

# row ii -> ii/L
# Then the freq of row ii is
freq[ii] = ii/Tn

```


This repository has been forked from https://bitbucket.org/cleemesser/stockwelltransform

Code from the NIH core imaging group MEG
http://kurage.nimh.nih.gov/meglab/Meg/Stockwell

**Note**, the NIH imaging center also has multidimensional stockwell transforms



