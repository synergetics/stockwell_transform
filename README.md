Stockwell Transform
======

![Sample Image](https://raw.githubusercontent.com/synergetics/stockwell_transform/master/examples/Multi-taper%20Stockwell%20transform%20spectrogram.png)

## Contains
1. c code
- python module

## Requirements for compilation

GCC
```bash
sudo apt-get install gcc
```

fftw3 libraries

```bash
sudo apt-get install libfftw3-dev
```

numpy (tested with 1.3)
```bash
sudo pip install numpy
```

## Build and Install

```bash
python ./setup.py build
sudo python ./setup.py install
```


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

## Origin

Code from Dr. Stockwell's web site for the stockwell transform

http://www.cora.nwra.com/~stockwel/index.php?module=fatcat&fatcat[user]=viewCategory&fatcat_id=2&module_title=pagemaster

Stockwell, R.G, L mansinha, and R. P. Lowe. Localization of the complex spectrum: The S-Transform. IEEE Transactions on Signal Processing, 44(4) pp998--1001, 1996.

This repository has been forked from https://bitbucket.org/cleemesser/stockwelltransform

C Code from the NIH core imaging group MEG
http://kurage.nimh.nih.gov/meglab/Meg/Stockwell

**Note**, the NIH imaging center also has multidimensional stockwell transforms


## FAQ

- How do I use it on windows? http://www.getgnulinux.org

