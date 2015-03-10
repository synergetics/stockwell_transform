# -*- coding: utf-8 -*-
"""
Created on Mon Jan 03 19:19:16 2011

@author: Chris Lee-Messer
"""
import numpy as np
import stockwell.smt as smt
import stockwell
Fs = 200
P = 1.0/Fs
T = 10.0
t = np.arange(0,T,P)
L = len(t)
twopi = 2*3.1415

# create a list of different sin waves at different frequencies
ss = [np.sin(twopi*f*t) for f in [5,10,20,30,50]]
y = np.zeros(L,dtype='float64')

for s in ss:  y+= s

sy = smt.st(y)
rsy = abs(sy)
sy10 = smt.st(y,0,100)
rsy10 = abs(sy10)


K=4
lowf, hif = 0,500
tapers = smt.calc_tapers(K,L)
mty = smt.mtst(K, tapers, y, lowf,hif)

# dsplay with
# figure(); imshow(mty); axis('auto')

# which rows have which frequencies?
freqticks = [stockwell.st_rowfreq(rr, Fs, L) for rr in [100,200,300,400,500]]

# visualization
import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox
from matplotlib.cbook import get_sample_data
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import host_subplot

f = plt.figure()
# extent = 0, T, 0, Fs/2.0
# plt.imshow(rsy,extent=extent,aspect='auto', origin='lower')

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

if 0:
    f = plt.figure()
    fa = plt.subplot(311)
    plt.plot(y)
    ax=plt.subplot(312)
    # plt.setp(ax, yticks=[10,25,50])
    plt.imshow(rsy,aspect='auto')
    plt.ylabel('frequency(Hz)')
    yloc,ylab=plt.yticks()
    plt.title('Stockwell transform spectrogram')
    phase1 = plt.subplot(313)

if 0:
    f2 = plt.figure()
    fa2 = plt.subplot(211)
    plt.plot(y)
    ax2_212=plt.subplot(212)
    # plt.setp(ax, yticks=[10,25,50])
    plt.imshow(mty,aspect='auto')
    plt.ylabel('frequency(Hz)')
    yloc2,ylab2=plt.yticks()
    plt.title("multi-taper stockwell transform spectrogram")


# divider = make_axes_locatable(ax)
#cax = divider.append_axes("right", size="5%", pad=0.05)



