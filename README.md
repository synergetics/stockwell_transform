Stockwell Transform
======

![Sample Image](https://raw.githubusercontent.com/synergetics/stockwell_transform/master/examples/Multi-taper%20Stockwell%20transform%20spectrogram.png)

## Contains
1. c code
- python module

## Requirements for compilation

fftw3 libraries

```bash
(sudo) apt-get install libfftw3-dev python3-dev
(sudo) pip install numpy
```

## Build and Install

```bash
(sudo) pip install stockwell
```

## Usage

```python

import numpy as np
import stockwell.smt as smt
import stockwell

import matplotlib.pyplot as plt

Fs = 200 # frequency
P = 1.0/Fs # time steps
T = 10.0 # max time
t = np.arange(0,T,P) # generate a time sequence
L = len(t)
twopi = 2*np.pi

# create a list of different sin waves at different frequencies
ss = [np.sin(twopi*f*t) for f in [5,10,20,30,50]]
y = np.zeros(L,dtype='float64')

for s in ss:
    y += s

# get the stockwell transform
sy = smt.st(y)
rsy = abs(sy)

f = plt.figure()

def plotspec(psx, fs, lofreq=None, hifreq=None, t1=None, t2=None):
    extent = [0,psx.shape[1], 0.0, fs/2.0]
    if t1 != None and t2 != None:
        extent[0] = t1
        extent[1] = t2
    if lofreq != None:
        extent[2] = lofreq
    if hifreq != None:
        extent[3] = hifreq

    return plt.imshow(psx, extent=extent, aspect='auto', origin='lower')

plotspec(rsy, fs=Fs, t1=0, t2=T)
plt.show()

```

![Sample](https://raw.githubusercontent.com/synergetics/stockwell_transform/master/examples/synthetic2.png)

## Origin

Code from Dr. Stockwell's web site for the stockwell transform

```
Stockwell, R.G, L mansinha, and R. P. Lowe. Localization of the complex spectrum: The S-Transform. IEEE Transactions on Signal Processing, 44(4) pp998--1001, 1996.
```

This repository has been forked from https://bitbucket.org/cleemesser/stockwelltransform

C Code from the NIH core imaging group MEG
http://kurage.nimh.nih.gov/meglab/Meg/Stockwell

**Note**, the NIH imaging center also has multidimensional stockwell transforms


## FAQ

- How do I use it on windows? http://www.getgnulinux.org

