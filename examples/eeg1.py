#log# Automatic Logger file. *** THIS MUST BE THE FIRST LINE ***
#log# DO NOT CHANGE THIS LINE OR THE TWO BELOW
#log# opts = Struct({'__allownew': True, 'logfile': 'ipython_log.py', 'pylab': 1})
#log# args = []
#log# It is safe to make manual edits below here.
#log#-----------------------------------------------------------------------
_ip.magic("colors NoColor")
from __future__ import division
import _edflib
import stockwell.smt as smt
_ip.magic("pwd ")
_ip.magic("cd /mnt/hgfs/")
_ip.magic("cd User")
_ip.system("ls -F ")
_ip.magic("cd clee")
_ip.magic("cd Documents/")
_ip.magic("cd swaineeg/")
_ip.system("ls -F ")
_ip.magic("cd NKT/")
_ip.system("ls -F ")
_ip.magic("cd EEG2100/")
_ip.system("ls -F ")
e=_edflib.Edfreader('CA75510M_1-1+_1-2+.edf')
# read a short number of samples
a = zeros(2000.0)
e.readsignal(0,0,2000,a)
plot(a)
K=20
N=2000
tapers = smt.calc_tapers(K,N)
s=smt.mtst(K,tapers,a)
s=smt.mtst(K,tapers,a,0,1000)

K
s.shape
figure()
imshow(s)
import scipy.signal as signal
signal.chirp 
#?signal.chirp
t=lin(0,10,n=1000)
t=linspace(0,10,n=1000)
t=linspace(0,10,1000)
t
ch = signal.chirp(t,1.0,6.0,20.0)
figure()
plot(t,ch)
chs = smt.mtst(K,tapers, ch, 0,len(ch)/2)
chtapers = smt.calc_tapers(K,len(ch))
chs = smt.mtst(K,chtapers, ch, 0,len(ch)/2)
figure(); imshow(chs)
figure(); subplot(211); plot(ch); subplot(212); imshow(chs)
## now try a longer signal
la=zeros(10000,dtype='float64')
#?smt.st
e.readsignal(0,0,len(la),la)
figure();plot(la)
las = smt.st(la)
figure(); plot(las)

figure(); imshow(las)
las.shape
las.dtype
lasre = np.abs(las)
lasre.shape
lasre.dtype
figure(); imshow(lasre)
MemoryError 
figure(); imshow(lasre[0:100,0:2000])
figure(); imshow(lasre[0:500,0:2000])
figure(); imshow(lasre[0:500,0:5000])
_ip.magic("logstart ")

