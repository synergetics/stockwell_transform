"""
provide matplotlib-based visualization functions for stockwell transforms
"""
import stockwell
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, \
     AnnotationBbox

from mpl_toolkits.axes_grid1 import host_subplot

def _get_specgram_plot_extents(psx, fs=2.0, lofreq=None, hifreq=None, t0=None, t1=None):
    """utility funciton to figure out plot extents for a spectrogram
    betwee times t0 and t1
    with lofreq and hifreq along y axis
    and power spectrum psx"""
    extent = [0,psx.shape[1]/float(fs), 0.0, fs/2.0] # default extents
    if t0 != None and t1 != None:
        extent[0] = t0
        extent[1] = t1
    if lofreq != None:
        extent[2] = lofreq
    if hifreq != None:
        extent[3] = hifreq
    return extent

def plotspec(psx, fs=2.0, lofreq=None, hifreq=None, t0=None, t1=None):
    """
    useful for plotting the power of a stockwell transform
    it relies upon matplotlib for display
    example:
    # for a signal x, with sampling frequency 200
    >>> import stockwell, pylab
    >>> import stockwell.plots as plots
    >>> x = pylab.zeros(1000.0) # 5 seconds
    >>> fs = 200 # sample rate
    >>> x[250:350] = 1.0 # step function
    >>> sx = stockwell.st(x)
    >>> psx = abs(sx) # create power
    >>> r=plots.plotspec(psx,200)
    >>> # pylab.show() # to visualize this
    """
    extent = [0,psx.shape[1]/float(fs), 0.0, fs/2.0] # default extents
    if t0 != None and t1 != None:
        extent[0] = t0
        extent[1] = t1
    if lofreq != None:
        extent[2] = lofreq
    if hifreq != None:
        extent[3] = hifreq
    plt.ylabel('Hz')
    #return plt.imshow(psx, extent=extent, aspect='auto', origin='lower')
    return plt.imshow(psx, aspect='auto', origin='lower')




def stspecgram(x,fs,lofreq=None, hifreq=None, t0=None, t1=None):
    """
    plot out the stockwell spectrum abs(st(x))
    given frequency sampling fs in Hz

    lofreq and hifreq are the frequency limits expressed in terms of the nyquist frequency(?)
    """

    n = x.shape[0]
    if t0==None:
        t0=0.0
    if t1==None:
        t1=n/float(fs)+t0

    if lofreq==None and hifreq==None:
        sx=stockwell.st(x)
        return plotspec(abs(sx),fs, t0=t0,t1=t1)

    lorow=stockwell.stfreq(lofreq,n,fs)
    hirow=stockwell.stfreq(hifreq,n,fs)
    sx=stockwell.st(x, lorow,hirow)
    return plotspec(abs(sx), fs, lofreq=lofreq,hifreq=hifreq, t0=t0,t1=t1)




def stpowerstack(x,stx):
    """
    need to add row labels
    """
    ax1=host_subplot(211)
    plt.plot(x)
    ax2 = host_subplot(212)
    #pax2 = ax2.twinx()
    #pax2.set_ylabel('frequency(Hz)')
    plt.imshow(abs(stx), aspect='auto')
    plt.ylabel('frequency(Hz)')
    ylocs,ylabels = plt.yticks()
    #plt.ylabel('st-row(f*L/fs)')
    yt,xt = stx.shape
    plt.show()

    return ax2


def timefreqplot(x,fs, lo=0,hi=0,title=None):
    """
    plot a signal and its spectrogram
    defaultis to find the entire frequency band (lo->0.0, hi-> n/2)

    lo (Hz) gets transformed to the sample-based lo_n for use with stockwell.st
    hi (Hz)
    """
    n = len(x)
    if not hi:
        hi_n = int(n/2) # float(fs/2)
        hi = fs/2.0
    else:
        hi_n = stockwell.stfreq(hi, n, fs)
        print("stfreq(hi,n,fs):", hi)
    print("setting hi", hi, hi_n)

    if not lo:
        lo = 0.0
        lo_n = 0
    else:
        lo_n = stockwell.stfreq(lo, n, fs)
        print("stfreq(lo,n,fs):", lo)
    print("setting low", lo, lo_n)

    fig,ax = plt.subplots(nrows=2,ncols=1, sharex=True)

    if title: ax.set_title(title)
    psx = abs(stockwell.st(x,lo_n,hi_n))
    print("psx.shape:", psx.shape)
    si = 1.0/fs
    ax[0].plot(np.arange(0,n)*si, x)

    #extents =  _get_specgram_plot_extents(psx, fs=fs, lofreq=lo, hifreq=hi,t0=0, t1=n/float(fs))
    extents = _get_specgram_plot_extents(psx, fs=fs, lofreq=lo, hifreq=hi,t0=0, t1=n/float(fs))
    print(extents)
    ax[1].set_ylabel('Hz')
    ax[1].imshow(psx, extent=extents,aspect='auto', origin='lower')
    return fig, ax, psx



if __name__ == "__main__":
    import doctest
    doctest.testmod()
