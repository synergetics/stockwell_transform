from pylab import *
import scipy.signal as signal
import stockwell.plots

signal.chirp 
#?signal.chirp
N = 1000
t=linspace(0,10,num=N) # implies fs=1000/10 = 100
fs = 100
ch = signal.chirp(t,1.0,6.0,20.0)

stockwell.plots.stspecgram(ch, 100,t0=0,t1=10.0)
title('chirp spectrum using the stockwell transform')

# figure()
# print "same signal but now focusing on 5-20Hz"
# stockwell.plots.stspecgram(ch, 100, lofreq=5,hifreq=20, t0=0,t1=10)

#
figure()
specgram(ch, Fs=fs)
