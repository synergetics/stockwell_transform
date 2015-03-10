"""
modules:
st  - link to C implementation
smt - multitaper stockwell transform 
get from st module:

hilbert(x) returns the complex Hilbert transform of the real array x.

st(x[, lo, hi]) returns the 2d, complex Stockwell transform of the real\n\
array x. If lo and hi are specified, only those frequencies (rows) are\n\
returned; lo and hi default to 0 and n/2, resp., where n is the length of x.

ist(y[, lo, hi]) returns the inverse Stockwell transform of the 2d, complex\n\
array y.

"""
from __future__ import division

# import the methods implemented in C
from st import st, ist, hilbert

def stfreq(f,length, srate):
	"""
        [int] = stfreq(f,length, srate)
        Convert frequencies f in Hz into rows of the stockwell transform
	given sampling rate srate and length of original array

        note: length * (1.0/srate)
      	# in C this would be:  return floor(f * len / srate + .5);
        
        """
        # return int( f*(length//srate)+0.5)
	return int(round(f*length/srate))

# row = int(f*length)/srate)
# row*srate = f*length
# f = row*srate/length

def st_rowfreq(row,srate,length):
	"""
	for a row in a stockwell transform, give what frequency (Hz)
	it corresponds to, given the sampling rate srate and the length of the original
	array
	"""
	return row*srate/length

# utilites/display functions in plot
