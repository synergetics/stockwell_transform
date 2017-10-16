from pylab import *
import scipy.signal as signal
import stockwell.smt as smt

signal.chirp
#?signal.chirp
t=linspace(0,10,num=1000)
ch = signal.chirp(t,1.0,6.0,20.0)
#figure()
#plot(t,ch)
K=4; N=len(t)
tapers = smt.calc_tapers(K,N)
chs = smt.mtst(K,tapers, ch, 0,len(ch)/2)
chtapers = smt.calc_tapers(K,len(ch))
chs = smt.mtst(K,chtapers, ch, 0,len(ch)/2)

# these don't quite look right
#figure(); imshow(chs); axis('auto')
#figure(); subplot(211); plot(ch); subplot(212); imshow(chs); axis('auto')
## now try a longer signal

import stockwell.plots as stplot

print "powerstack of multitaper version of signal"
stplot.stpowerstack(ch, chs)
