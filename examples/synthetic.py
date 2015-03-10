#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on Mon Jan 03 19:19:16 2011

@author: Chris Lee-Messer
"""

import numpy as np
import stockwell.smt as smt
import stockwell

# visualization
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data

Fs = 100
T = 1.0
t = np.arange(0,T, T/Fs)
L = len(t)
twopi = 2*3.1415

# create a list of different sin waves at different frequencies
ss = [np.sin(twopi*f*t) for f in [5,10,20,30,40,50,100,200,400]]
y = np.zeros(L,dtype='float64')

for s in ss:
  y+= s

sy = smt.st(y)
rsy = abs(sy)
sy10 = smt.st(y,0,100)
rsy10 = abs(sy10)


K=4

tapers = smt.calc_tapers(K,L)
mty = smt.mtst(K, tapers, y, 0,70)

# which rows have which frequencies?
freqticks = [stockwell.st_rowfreq(rr, Fs, L) for rr in [100,200,300,400,500]]

f = plt.figure()
fa = plt.subplot(211)
plt.plot(y)
ax=plt.subplot(212)
# plt.setp(ax, yticks=[10,25,50])
plt.imshow(rsy,aspect='auto')
plt.ylabel('frequency(Hz)')
plt.savefig('synthetic.png')
plt.show()
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="5%", pad=0.05)


