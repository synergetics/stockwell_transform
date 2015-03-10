#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on Mon Jan 03 19:19:16 2011

@author: Chris Lee-Messer
"""

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

# get the stockwell transform with frequencies between 1 and 100
sy10 = smt.st(y,0,100)
rsy10 = abs(sy10)

# multi-tapers
K=4
lowf, hif = 0,500
tapers = smt.calc_tapers(K,L)
mty = smt.mtst(K, tapers, y, lowf,hif)

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
plt.savefig('synthetic2.png')

f = plt.figure()
fa = plt.subplot(311)
plt.plot(y)
ax=plt.subplot(312)
# plt.setp(ax, yticks=[10,25,50])
plt.imshow(rsy,aspect='auto')
plt.ylabel('frequency(Hz)')
yloc,ylab=plt.yticks()
plt.title('Stockwell transform spectrogram')
plt.savefig("Stockwell transform spectrogram.png")
phase1 = plt.subplot(313)

f2 = plt.figure()
fa2 = plt.subplot(211)
plt.plot(y)
ax2_212=plt.subplot(212)
# plt.setp(ax, yticks=[10,25,50])
plt.imshow(mty,aspect='auto')
plt.ylabel('frequency(Hz)')
yloc2,ylab2=plt.yticks()
plt.title("multi-taper stockwell transform spectrogram")
plt.savefig("Multi-taper Stockwell transform spectrogram.png")

plt.show()

