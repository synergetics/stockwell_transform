from __future__ import division
from numpy import *
from matplotlib.pyplot import *

import _edflib
import stockwell.smt as smt
# eegfile="/mnt/hgfs/clee/Documents/swaineeg/NKT/EEG2100/CA75510M_1-1+_1-2+.edf"
eegfile='/home/clee/Dropbox/data/swainAFIB_CA46803E_1-1+.edf'
eegfile=r'/home/clee/Dropbox/data/swainShortAFIB_CA46803D_1-1+_1-2+.edf'
open(eegfile)
e=_edflib.Edfreader(eegfile)

def showst(swtransform, newfigure=True):
    if newfigure:
        figure()
    imshow(swtransform, origin='lower', aspect='auto')
    #axis('auto')
    

# read a short number of samples


import scipy.signal as signal
#?signal.chirp
t=linspace(0,10,num=1000)
chrp = signal.chirp(t)

pstchrp = abs(smt.st(chrp))
showst(pstchrp)



eeg2000= zeros(2000.0)
e.readsignal(0,0,2000,eeg2000)
e.close()
