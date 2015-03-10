from __future__ import division
from numpy import *
from matplotlib.pyplot import *

import _edflib
import stockwell.smt as smt
# eegfile="/mnt/hgfs/clee/Documents/swaineeg/NKT/EEG2100/CA75510M_1-1+_1-2+.edf"
eegfile='/home/clee/Dropbox/data/swainAFIB_CA46803E_1-1+.edf'
open(eegfile)
e=_edflib.Edfreader(eegfile)

# read a short number of samples
a = zeros(2000.0)
e.readsignal(0,0,2000,a)
plot(a)
K=4
N=2000
tapers = smt.calc_tapers(K,N)
#s=smt.mtst(K,tapers,a)
s=smt.mtst(K,tapers,a,0,70)

figure(); imshow(s); axis('auto')

la=zeros(10000,dtype='float64')
#?smt.st
e.readsignal(0,0,len(la),la)
figure();plot(la)
las = smt.st(la, 0,70)
#figure(); plot(las)
rlas = abs(las)

figure(); imshow(rlas); axis('auto')
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

