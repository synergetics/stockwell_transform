from pylab import *
import scipy.signal as signal
import stockwell.plots

N = 1000
t=linspace(0,10,num=N) # implies fs=1000/10 = 100
fs = 100
ch = signal.chirp(t,1.0,6.0,20.0)

stockwell.plots.stspecgram(ch, 100,t0=0,t1=10.0)
title('chirp spectrum using the stockwell transform')
savefig('chirp spectrum using the stockwell transform.png')

#
figure()
specgram(ch, Fs=fs)
savefig('chirp spectogram using the stockwell transform')
show()
